# Dadosfera Project - Prioritized Task List

**Project**: Dadosfera Name-to-Video Pipeline  
**Goal**: Type a name → Get professional 3D video with realistic explosions  
**Last Updated**: 2025-10-03

---

## 🎯 Mission

Create an end-to-end pipeline that transforms text input (company/product names) into professional 3D videos featuring:
1. Extruded 3D text/logo with materials
2. Cinematic camera movement
3. Realistic explosion effects
4. Professional lighting and composition
5. High-quality rendered output (1080p H.264)

---

## 📊 Current Status

- **Phase**: Integration & Testing
- **Progress**: ~70% complete
- **Blockers**: Explosion integration validation pending
- **Next Milestone**: End-to-end demo video

### Completed ✅
- [x] Render service architecture (`RENDER_SERVICE.md`)
- [x] Quality presets (quick/preview/production/final)
- [x] Blender scene setup with camera and lighting
- [x] Export naming conventions (`exports/RENAME_GUIDE.md`)
- [x] Render history tracking (`RENDER_HISTORY.md`)
- [x] FFmpeg encoding pipeline

### In Progress 🔄
- [ ] Text-to-3D extrusion system
- [ ] Explosion integration with timing
- [ ] API endpoint for full pipeline

### Pending ⏳
- [ ] Material system for text/logo
- [ ] Automated camera path generation
- [ ] Quality validation framework
- [ ] Production deployment

---

## 🚀 Prioritized Execution Queue

### **P0: CRITICAL PATH** (Week 1 - Must Complete)

#### 1. Finalize Text-to-3D Extrusion Pipeline
**Owner**: Logo-to-3D Service  
**Depends on**: `docs/plans/active/logo-to-3d-service.md`  
**Tasks**:
- [ ] Text input → Blender text object creation
- [ ] Font selection and loading system
- [ ] Extrusion depth and bevel configuration
- [ ] Material assignment (metallic/glossy)
- [ ] Position/scale/rotation setup
- [ ] Test with 5+ sample names

**Success Criteria**:
- Takes text string, returns 3D object in scene
- Supports custom fonts
- Consistent scale and positioning
- Materials look professional

**Estimated Time**: 3-4 days

---

#### 2. Integrate Explosions into Name Scene
**Owner**: VFX Team  
**Depends on**: `docs/plans/active/explosion-development-roadmap.md`  
**Tasks**:
- [ ] Import explosion system into dadosfera scene
- [ ] Position explosions around text object
- [ ] Set explosion timing (e.g., frames 50, 70, 90)
- [ ] Adjust explosion scale for scene
- [ ] Test lighting interactions
- [ ] Validate render performance

**Success Criteria**:
- 3-5 explosions positioned cinematically
- Explosions don't obscure text completely
- Lighting enhances text visibility
- Render time <20s/frame at medium quality

**Estimated Time**: 2-3 days

---

#### 3. Validate End-to-End Pipeline
**Owner**: Integration Team  
**Depends on**: Tasks #1 and #2  
**Tasks**:
- [ ] Create test script: name → video
- [ ] Run full pipeline with "DADOSFERA" text
- [ ] Render 10 validation keyframes
- [ ] Encode to video (1080p H.264)
- [ ] Review for quality issues
- [ ] Document any bugs/issues

**Success Criteria**:
- Full pipeline runs without manual intervention
- Output video is professional quality
- Total time <30 minutes (for medium quality)
- No critical artifacts or errors

**Estimated Time**: 2 days

---

### **P1: HIGH PRIORITY** (Week 2 - Important)

#### 4. Create API Endpoint for Pipeline
**Owner**: Logo-to-3D Service  
**Depends on**: Task #3 (validation)  
**Tasks**:
- [ ] FastAPI endpoint: `POST /api/render/name-video`
- [ ] Request body: `{ "text": "...", "quality": "...", "duration": ... }`
- [ ] Background job handling (async render)
- [ ] Progress tracking endpoint
- [ ] Result delivery (video URL or direct download)
- [ ] Error handling and retries

**Success Criteria**:
- API accepts text input
- Returns job ID immediately
- Polls for completion
- Downloads rendered video
- Handles errors gracefully

**Estimated Time**: 3-4 days

---

#### 5. Implement Material System
**Owner**: VFX Team  
**Tasks**:
- [ ] Define material presets (metallic, glass, plastic, etc.)
- [ ] Material parameter configuration (roughness, metallic, color)
- [ ] Material library JSON format
- [ ] Apply materials to text object
- [ ] Test with different lighting conditions

**Success Criteria**:
- 5+ material presets available
- Materials look photorealistic
- Easy to switch between presets
- Compatible with explosion lighting

**Estimated Time**: 2-3 days

---

#### 6. Automated Camera Path Generation
**Owner**: VFX Team  
**Tasks**:
- [ ] Define camera movement presets (orbit, dolly, crane)
- [ ] Calculate camera positions based on text size
- [ ] Generate smooth animation curves
- [ ] Avoid collision with explosions
- [ ] Test with various text lengths

**Success Criteria**:
- Camera shows text from best angles
- Movement is smooth and professional
- Adapts to text dimensions
- Keeps explosions in frame

**Estimated Time**: 2-3 days

---

### **P2: MEDIUM PRIORITY** (Week 3-4 - Nice to Have)

#### 7. Quality Validation Framework
**Owner**: QA  
**Tasks**:
- [ ] Define quality metrics (resolution, artifacts, timing)
- [ ] Automated frame analysis (brightness, contrast, sharpness)
- [ ] Manual review checklist
- [ ] Pass/fail criteria documentation
- [ ] Integration with CI/CD (if applicable)

**Estimated Time**: 2 days

---

#### 8. Performance Optimization
**Owner**: Dev Team  
**Tasks**:
- [ ] Profile render bottlenecks
- [ ] Optimize particle counts for quality/speed balance
- [ ] Implement adaptive sampling
- [ ] Cache frequently used assets
- [ ] Document performance tuning guide

**Estimated Time**: 3-4 days

---

#### 9. Additional Explosion Presets
**Owner**: VFX Team  
**Tasks**:
- [ ] Small/Medium/Large explosion size presets
- [ ] Different timing patterns (rapid fire, staggered, finale burst)
- [ ] Color variations (blue fire, green explosions, etc.)
- [ ] Intensity levels (subtle → dramatic)

**Estimated Time**: 2-3 days

---

#### 10. User Documentation
**Owner**: Docs Team  
**Tasks**:
- [ ] API usage guide
- [ ] Parameter reference
- [ ] Example gallery (input → output samples)
- [ ] Troubleshooting guide
- [ ] Performance tips

**Estimated Time**: 2 days

---

### **P3: LOW PRIORITY** (Backlog - Future)

#### 11. Logo Upload Support
- [ ] Image upload endpoint
- [ ] SVG/PNG to 3D conversion
- [ ] Logo tracing and vectorization
- [ ] Custom texture mapping

#### 12. Audio Integration
- [ ] Background music selection
- [ ] Explosion sound effects
- [ ] Audio sync with explosions
- [ ] Volume normalization

#### 13. Advanced Camera Features
- [ ] Multi-camera angles
- [ ] Picture-in-picture effects
- [ ] Slow motion during explosions
- [ ] Custom camera keyframes

#### 14. Batch Processing
- [ ] Process multiple names in one request
- [ ] Bulk video generation
- [ ] Queue management
- [ ] Parallel rendering

#### 15. Cloud Deployment
- [ ] Containerization (Docker)
- [ ] Cloud storage for outputs
- [ ] Scalable render farm
- [ ] CDN for video delivery

---

## 📈 Progress Tracking

### Sprint Velocity
- **Week 1 Target**: Complete P0 tasks (3 tasks)
- **Week 2 Target**: Complete P1 tasks (4 tasks)
- **Week 3-4 Target**: Complete P2 tasks (4 tasks)

### Milestones
| Milestone | Target Date | Status | Dependencies |
|-----------|-------------|--------|--------------|
| Text-to-3D working | End of Week 1 | 🔄 In Progress | Logo-to-3D service |
| Explosions integrated | End of Week 1 | ⏳ Pending | Explosion roadmap |
| End-to-end demo | End of Week 1 | ⏳ Pending | Tasks #1-3 |
| API deployed | End of Week 2 | ⏳ Pending | Task #4 |
| Material system complete | End of Week 2 | ⏳ Pending | Task #5 |
| Production ready | End of Week 4 | ⏳ Pending | All P0-P2 tasks |

---

## 🔗 Related Documentation

- **Project Overview**: `projects/dadosfera/README.md`
- **Render Service**: `projects/dadosfera/RENDER_SERVICE.md`
- **Render History**: `projects/dadosfera/RENDER_HISTORY.md`
- **Export Guide**: `projects/dadosfera/exports/RENAME_GUIDE.md`
- **Project Structure**: `projects/dadosfera/PROJECT_STRUCTURE.md`

### Active Plans
- **Logo-to-3D Service**: `docs/plans/active/logo-to-3d-service.md`
- **Explosion Development**: `docs/plans/active/explosion-development-roadmap.md`
- **Dependency Map**: `docs/plans/active/DEPENDENCY_MAP.md`

---

## 🚨 Blockers & Risks

### Current Blockers
1. **Explosion Integration Validation** (P0, Task #2)
   - **Impact**: Blocks end-to-end demo
   - **Resolution**: Complete `projects/explosion-test/VALIDATION_CHECKLIST.md`
   - **ETA**: 2-3 days

### Risks
1. **Render Performance** (Medium Risk)
   - May exceed 20s/frame with complex scenes
   - **Mitigation**: Use quick quality for previews, optimize materials
   
2. **API Scalability** (Low Risk)
   - Single-threaded renders may bottleneck
   - **Mitigation**: Queue system, background workers, cloud scaling

3. **Quality Consistency** (Medium Risk)
   - Different text lengths may require different camera/explosion settings
   - **Mitigation**: Test with diverse inputs, create adaptive logic

---

## 📞 Contacts & Ownership

| Area | Owner | Contact |
|------|-------|---------|
| Overall Project | Product Lead | TBD |
| Text-to-3D Pipeline | Logo-to-3D Service Team | See `logo-to-3d-service.md` |
| Explosion Effects | VFX Team | See `explosion-development-roadmap.md` |
| Render Service | DevOps | See `RENDER_SERVICE.md` |
| API Development | Backend Team | TBD |
| Documentation | Docs Team | TBD |

---

**Next Review**: Weekly on Mondays  
**Status Updates**: Daily standups or async in project channel  
**Escalation Path**: Blockers → Team Lead → Product Lead
