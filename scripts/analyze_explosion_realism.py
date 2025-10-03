#!/usr/bin/env python3
"""
Analyze explosion realism and provide specific improvements
This script identifies common issues that make explosions look fake
"""

import bpy
import bmesh
from mathutils import Vector


def analyze_current_explosions():
    """Analyze current explosion setup for realism issues"""
    print("\n" + "=" * 80)
    print("🔍 EXPLOSION REALISM ANALYSIS")
    print("=" * 80 + "\n")

    # Check for common issues
    issues = []
    recommendations = []

    # 1. Check materials
    print("📋 MATERIAL ANALYSIS:")
    fire_materials = 0
    emission_materials = 0
    volume_materials = 0

    for mat in bpy.data.materials:
        if "Fire" in mat.name or "Explosion" in mat.name:
            fire_materials += 1
            print(f"   Fire material: {mat.name}")

            if mat.use_nodes:
                nodes = mat.node_tree.nodes
                has_emission = any(node.type == 'EMISSION' for node in nodes)
                has_volume = any(node.type == 'VOLUME' for node in nodes)

                if has_emission:
                    emission_materials += 1
                    print(f"     ✅ Has emission shader")
                else:
                    issues.append("Missing emission shaders for fire")
                    recommendations.append(
                        "Add emission shaders with high strength for fire glow")

                if has_volume:
                    volume_materials += 1
                    print(f"     ✅ Has volume shader")
                else:
                    print(f"     ⚠️  No volume shader (needed for smoke)")

    # 2. Check particle systems
    print(f"\n📋 PARTICLE SYSTEM ANALYSIS:")
    particle_systems = 0
    for obj in bpy.data.objects:
        if obj.particle_systems:
            particle_systems += len(obj.particle_systems)
            print(f"   Object {obj.name}: {len(obj.particle_systems)} particle systems")

            for ps in obj.particle_systems:
                settings = ps.settings
                print(f"     Count: {settings.count}")
                print(f"     Lifetime: {settings.lifetime}")
                print(f"     Physics: {settings.physics_type}")

                if settings.count < 100:
                    issues.append(
                        f"Low particle count ({settings.count}) - explosions need hundreds of particles")
                    recommendations.append(
                        "Increase particle count to 500-1000 for realistic explosions")

                if settings.lifetime < 2.0:
                    issues.append(f"Short particle lifetime ({settings.lifetime})")
                    recommendations.append("Increase particle lifetime to 3-5 seconds")

                if settings.physics_type != 'NEWTON':
                    issues.append("Particles not using Newton physics")
                    recommendations.append(
                        "Use Newton physics for realistic particle motion")

    # 3. Check animation
    print(f"\n📋 ANIMATION ANALYSIS:")
    animated_objects = 0
    for obj in bpy.data.objects:
        if obj.animation_data and obj.animation_data.action:
            animated_objects += 1
            print(f"   Animated object: {obj.name}")

            # Check for scale animation
            has_scale_animation = False
            for fcurve in obj.animation_data.action.fcurves:
                if 'scale' in fcurve.data_path:
                    has_scale_animation = True
                    break

            if has_scale_animation:
                print(f"     ✅ Has scale animation")
            else:
                issues.append(f"Object {obj.name} missing scale animation")
                recommendations.append("Add scale animation for explosion growth")

    # 4. Check lighting
    print(f"\n📋 LIGHTING ANALYSIS:")
    lights = [obj for obj in bpy.data.objects if obj.type == 'LIGHT']
    print(f"   Number of lights: {len(lights)}")

    if len(lights) == 0:
        issues.append("No lights in scene")
        recommendations.append("Add area lights or sun light for proper illumination")
    elif len(lights) == 1:
        issues.append("Only one light - explosions need multiple light sources")
        recommendations.append(
            "Add multiple lights: main light, fire glow, rim lighting")

    # 5. Check camera and composition
    print(f"\n📋 CAMERA ANALYSIS:")
    camera = bpy.context.scene.camera
    if camera:
        print(f"   Camera: {camera.name}")
        print(f"   Location: {camera.location}")
        print(f"   Rotation: {camera.rotation_euler}")

        # Check if camera is too close or too far
        distance = camera.location.length
        if distance < 5:
            issues.append("Camera too close to explosion")
            recommendations.append("Move camera further back for better composition")
        elif distance > 20:
            issues.append("Camera too far from explosion")
            recommendations.append("Move camera closer for more dramatic effect")
    else:
        issues.append("No camera in scene")
        recommendations.append("Add camera for rendering")

    # 6. Check render settings
    print(f"\n📋 RENDER SETTINGS ANALYSIS:")
    scene = bpy.context.scene
    print(f"   Engine: {scene.render.engine}")
    print(f"   Resolution: {scene.render.resolution_x}x{scene.render.resolution_y}")

    if scene.render.engine == 'BLENDER_EEVEE':
        issues.append("Using Eevee - Cycles recommended for realistic explosions")
        recommendations.append(
            "Switch to Cycles for better volume rendering and fire effects")
    elif scene.render.engine == 'CYCLES':
        print(f"   Samples: {scene.cycles.samples}")
        if scene.cycles.samples < 128:
            issues.append("Low sample count - explosions need high quality rendering")
            recommendations.append(
                "Increase samples to 256-512 for realistic explosions")

        print(f"   Volume bounces: {scene.cycles.volume_bounces}")
        if scene.cycles.volume_bounces < 4:
            issues.append("Low volume bounces - smoke needs multiple bounces")
            recommendations.append(
                "Increase volume bounces to 8-12 for realistic smoke")

    # Summary
    print(f"\n📊 ANALYSIS SUMMARY:")
    print(f"   Fire materials: {fire_materials}")
    print(f"   Emission materials: {emission_materials}")
    print(f"   Volume materials: {volume_materials}")
    print(f"   Particle systems: {particle_systems}")
    print(f"   Animated objects: {animated_objects}")
    print(f"   Lights: {len(lights)}")

    if issues:
        print(f"\n❌ ISSUES FOUND ({len(issues)}):")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
    else:
        print(f"\n✅ No major issues found!")

    if recommendations:
        print(f"\n💡 RECOMMENDATIONS ({len(recommendations)}):")
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")

    return issues, recommendations


def create_realism_checklist():
    """Create a checklist for realistic explosions"""
    print(f"\n📋 REALISTIC EXPLOSION CHECKLIST:")
    print("=" * 50)

    checklist = [
        "✅ Fire particles with emission materials (bright orange/yellow)",
        "✅ Smoke volume with volume shader (dark gray/black)",
        "✅ Debris particles with physics (falling motion)",
        "✅ Multiple light sources (main + fire glow + rim)",
        "✅ Proper camera angle and distance",
        "✅ High sample count (256-512)",
        "✅ Volume bounces (8-12)",
        "✅ Particle count (500-1000)",
        "✅ Particle lifetime (3-5 seconds)",
        "✅ Scale animation (growth over time)",
        "✅ Color gradients (red → orange → yellow → white)",
        "✅ Noise textures for fire/smoke variation",
        "✅ Physics-based motion (gravity, velocity)",
        "✅ Multiple explosion layers (fire + smoke + debris)",
        "✅ Proper timing (fire first, then smoke, then debris)"
    ]

    for item in checklist:
        print(f"   {item}")

    print(f"\n🎯 COMMON REALISM ISSUES:")
    print("   1. Too few particles (looks sparse)")
    print("   2. No volume rendering (smoke looks flat)")
    print("   3. Poor lighting (explosion looks dark)")
    print("   4. No physics (particles don't move realistically)")
    print("   5. Wrong colors (fire should be red/orange, not blue)")
    print("   6. No scale animation (explosion doesn't grow)")
    print("   7. Low render quality (looks pixelated)")
    print("   8. No debris (explosion looks incomplete)")


def suggest_improvements():
    """Suggest specific improvements based on analysis"""
    print(f"\n🔧 SUGGESTED IMPROVEMENTS:")
    print("=" * 50)

    improvements = [
        "1. FIRE MATERIALS:",
        "   - Use emission shaders with high strength (20-50)",
        "   - Color gradient: Red → Orange → Yellow → White",
        "   - Add noise texture for variation",
        "   - Animate color over time",
        "",
        "2. SMOKE VOLUME:",
        "   - Use Volume Principled shader",
        "   - Dark gray/black color",
        "   - Multiple noise layers for complexity",
        "   - Animate density over time",
        "",
        "3. PARTICLE SYSTEMS:",
        "   - Increase count to 500-1000 particles",
        "   - Use Newton physics",
        "   - Lifetime 3-5 seconds",
        "   - Add turbulence for realistic motion",
        "",
        "4. LIGHTING:",
        "   - Main light (sun/area light)",
        "   - Fire glow (orange point light)",
        "   - Rim lighting (blue/white)",
        "   - Animate light intensity",
        "",
        "5. RENDER SETTINGS:",
        "   - Use Cycles engine",
        "   - 256-512 samples",
        "   - 8-12 volume bounces",
        "   - Enable denoising",
        "",
        "6. ANIMATION:",
        "   - Scale explosion over time",
        "   - Move particles outward",
        "   - Fade smoke over time",
        "   - Add camera shake"
    ]

    for improvement in improvements:
        print(f"   {improvement}")


def main():
    print("🔍 EXPLOSION REALISM ANALYZER")
    print("This script analyzes your explosion setup and identifies realism issues")
    print()

    issues, recommendations = analyze_current_explosions()
    create_realism_checklist()
    suggest_improvements()

    print(f"\n" + "=" * 80)
    print("📊 ANALYSIS COMPLETE!")
    print("=" * 80)

    if issues:
        print(
            f"Found {len(issues)} issues that may be making your explosions look unrealistic.")
        print("Follow the recommendations above to improve realism.")
    else:
        print("Your explosion setup looks good! Check the checklist for any missing elements.")

    print(f"\nNext steps:")
    print("1. Run create_improved_realistic_explosions.py for enhanced effects")
    print("2. Adjust render settings for higher quality")
    print("3. Test different camera angles")
    print("4. Add more particles if needed")
    print("5. Experiment with different materials")


if __name__ == "__main__":
    main()
