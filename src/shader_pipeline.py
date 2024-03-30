from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.app import App
    import pygame as pg


class ShaderPipeline:
    def __init__(self, app: "App", uniforms_map: dict={}, vert_shader_id: str="default", frag_shader_id: str="default", has_tex: bool=True):
        self.app = app
        self.ctx = app.ctx
        self.has_tex = has_tex
        self.image = self.ctx.image(self.app.screen_size, 'rgba8unorm')
        self.uniforms, self.ufs_size, self.ufs_includes = self.pack_uniforms(uniforms_map)
        self.uniform_buffer = self.ctx.buffer(size=self.ufs_size)
        layout, resources = self.get_resources_and_layout()

        self.pipeline = self.ctx.pipeline(
            includes=self.ufs_includes,
            vertex_shader=self.load_shader_src(f'{vert_shader_id}.vert'),
            fragment_shader=self.load_shader_src(f'{frag_shader_id}.frag'),
            layout=layout,
            resources=resources,
            framebuffer=None,
            topology='triangle_strip',
            viewport=(0, 0, *self.app.screen_size),
            vertex_count=4,
            blend={'enable': True, 'src_color': "src_alpha", 'dst_color': "one_minus_src_alpha"},
        )
    
    def get_resources_and_layout(self):
        layout = [{'name': 'Common', 'binding': 0}]
        resources = [{'type': 'uniform_buffer', 'binding': 0, 'buffer': self.uniform_buffer}]
        if self.has_tex:
            layout.append({'name': 'Texture', 'binding': 0})
            resources.append(
                {
                    'type': 'sampler',
                    'binding': 0,
                    'image': self.image,
                    'min_filter': 'nearest',
                    'mag_filter': 'nearest',
                    'wrap_x': 'clamp_to_edge',
                    'wrap_y': 'clamp_to_edge',
                }
            )
        return layout, resources

    def render(self, screen: "pg.Surface | None"=None):
        self.update_uniforms()
        if screen:
            screen_buffer = screen.get_view('0').raw
            self.image.write(screen_buffer)
        self.pipeline.render()


    def update_uniforms(self):
        if self.uniforms:
            for uniform in self.uniforms.values():
                self.uniform_buffer.write(uniform['value'](), offset=uniform['offset'])        

    @staticmethod
    def load_shader_src(shader_name: str) -> str:
        with open(f"src/shaders/{shader_name}") as f:
            return f.read()
        
    @staticmethod
    def pack_uniforms(uniforms_map: dict) -> tuple[dict, int, dict]:
        uniforms = {}
        layout = ""
        offset = 0
        for uf_name, uf_data in uniforms_map.items():
            if uf_data['glsl_type'] == 'float':
                size = 4  # Size of a float in bytes
                align = 4
            elif uf_data['glsl_type'] == 'vec2':
                size = 8  # 2 floats
                align = 8
            elif uf_data['glsl_type'] == 'vec3':
                size = 12  # 3 floats, but aligned as vec4 in std140 layout
                align = 16
            elif uf_data['glsl_type'] == 'vec4':
                size = 16  # 4 floats
                align = 16
            elif uf_data['glsl_type'] == 'mat4':
                size = 64 # 4x4 floats
                align = 16 # aligned as vec4 in std140 layout
            else:
                raise ValueError(f"Unknown GLSL type: {uf_data['glsl_type']}")

            # Add padding for alignment
            if offset % align != 0:
                offset += align - (offset % align)

            uniforms[uf_name] = {
                "value": uf_data['value'],
                "offset": offset
            }
            offset += size
            layout += f"{uf_data['glsl_type']} {uf_name};\n"

        includes = f'''
                layout (std140) uniform Common {{{layout if uniforms else 'float dummy;'}}};
            ''' 
        buffer_size = 16 + offset
        return uniforms, buffer_size, {"uniforms": includes.strip()}
