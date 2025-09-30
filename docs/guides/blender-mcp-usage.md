# Blender MCP Usage Guide

## Features

- **Object manipulation**: Create, modify, and delete 3D objects in Blender
- **Material control**: Apply and modify materials and colors
- **Scene inspection**: Get detailed information about the current Blender scene
- **Code execution**: Run Python code in Blender from Cursor
- **Poly Haven integration**: Download models, textures, and HDRIs
- **Hyper3D AI models**: Generate 3D models using AI
- **Viewport screenshots**: View Blender viewport to understand the scene

## Example Commands

Try asking Cursor things like:

### Scene Creation
- "Create a low poly scene in a dungeon, with a dragon guarding a pot of gold"
- "Create a beach vibe using HDRIs, textures, and models from Poly Haven"
- "Create a sphere and place it above the cube"

### Material & Appearance
- "Make this car red and metallic"
- "Add a glass material to the sphere with blue tint"
- "Create a glowing emission material with cyan color"

### Lighting & Camera
- "Make the lighting like a studio"
- "Point the camera at the scene, and make it isometric"
- "Add three-point lighting to the scene"
- "Create a cinematic camera angle"

### Animation
- "Create a helicopter-style camera orbit around the scene"
- "Animate the cube rotating 360 degrees over 5 seconds"
- "Add keyframes for the sphere to bounce up and down"

### AI & Assets
- "Generate a 3D model of a garden gnome through Hyper3D"
- "Download a stone texture from Poly Haven"
- "Add an HDRI environment from Poly Haven for outdoor lighting"

## Working with Projects

### Creating a New Project

1. Start Blender with MCP connected
2. Ask Cursor to create your scene
3. Save the Blender file in the appropriate project folder:
   - `projects/<project-name>/blender/<project-name>.blend`

### Rendering

For rendering frames and animations, see the [Rendering Guide](rendering-guide.md).

### Exporting

- Animation frames go to: `projects/<project-name>/renders/frames/`
- Still renders go to: `projects/<project-name>/renders/stills/`
- Final videos go to: `projects/<project-name>/exports/`

## Best Practices

1. **Save often**: The MCP executes arbitrary Python code, so save your work frequently
2. **Break down complex requests**: Instead of one large request, break it into smaller steps
3. **Use descriptive names**: Name objects clearly so the AI can reference them later
4. **Check viewport**: Use viewport screenshots to verify the scene state
5. **Test incrementally**: Create, test, refine - don't try to do everything at once

## Workflow Example

```
1. "Create a scene with a red sphere on a plane"
2. "Add a metallic gold cube next to it"
3. "Add studio lighting with three-point setup"
4. "Position the camera at an angle to see both objects"
5. "Render the current frame at 1920x1080"
6. "Create a 360-degree camera rotation animation over 10 seconds"
7. "Render frames 1, 60, 120, 180, and 240"
```

## Tips & Tricks

- Use specific measurements: "Create a cube scaled to 2.5 units"
- Specify exact colors: "Use RGB (0.8, 0.2, 0.1)"
- Reference objects by name: "Move the 'RedSphere' to position (5, 3, 1)"
- Ask for viewport screenshots to see progress
- Save complex scenes as .blend files for future work
