#!/bin/bash
# workflows/run.sh
# Detailed implementation for all Makefile operations

set -e  # Exit on error

# =============================================================================
# CONFIGURATION
# =============================================================================

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BLENDER="/Applications/Blender.app/Contents/MacOS/Blender"
PYTHON="python3"

# Paths
SCRIPTS_DIR="${PROJECT_ROOT}/scripts"
TESTS_DIR="${PROJECT_ROOT}/tests"
LOGS_DIR="${PROJECT_ROOT}/logs"
PROJECTS_DIR="${PROJECT_ROOT}/projects"
INTEGRATIONS_DIR="${PROJECT_ROOT}/integrations"

# Project-specific paths
DADOSFERA_BLEND="${PROJECTS_DIR}/dadosfera/blender_files/dadosfera_animation_v1_improved_explosions.blend"
EXPLOSION_BLEND="${PROJECTS_DIR}/explosion-test/blender_files/ultra_realistic_explosion.blend"
RENDER_SERVICE="${SCRIPTS_DIR}/render_service.py"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

print_header() {
    echo -e "${CYAN}========================================${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

check_blender() {
    if [ ! -f "${BLENDER}" ]; then
        print_error "Blender not found at ${BLENDER}"
        print_info "Run: python scripts/detect_blender.py"
        exit 1
    fi
}

check_file() {
    if [ ! -f "$1" ]; then
        print_error "File not found: $1"
        exit 1
    fi
}

# =============================================================================
# SETUP & VALIDATION
# =============================================================================

cmd_check() {
    print_header "Checking Environment"
    
    # Check Blender
    if [ -f "${BLENDER}" ]; then
        print_success "Blender found at ${BLENDER}"
        ${BLENDER} --version | head -1
    else
        print_warning "Blender not found at default location"
    fi
    
    # Check Python
    print_info "Python version:"
    ${PYTHON} --version
    
    # Run detection script
    if [ -f "${SCRIPTS_DIR}/detect_blender.py" ]; then
        print_info "Running Blender detection..."
        ${PYTHON} "${SCRIPTS_DIR}/detect_blender.py"
    fi
    
    print_success "Environment check complete"
}

cmd_validate() {
    print_header "Running All Validations"
    cmd_validate_docs
    cmd_validate_taxonomy
    cmd_validate_json
    cmd_validate_links
    print_success "All validations complete"
}

cmd_validate_docs() {
    print_info "Validating documentation..."
    ${PYTHON} "${SCRIPTS_DIR}/validate_docs.py"
}

cmd_validate_taxonomy() {
    print_info "Validating project taxonomy..."
    ${PYTHON} "${SCRIPTS_DIR}/validate_taxonomy.py"
}

cmd_validate_json() {
    print_info "Validating JSON files..."
    ${PYTHON} "${SCRIPTS_DIR}/validate_json.py"
}

cmd_validate_links() {
    print_info "Validating markdown links..."
    ${PYTHON} "${SCRIPTS_DIR}/validate_links.py"
}

# =============================================================================
# TESTING
# =============================================================================

cmd_test() {
    print_header "Running Tests (excluding Blender tests)"
    cd "${PROJECT_ROOT}"
    pytest tests/ -v -m "not blender"
}

cmd_test_unit() {
    print_header "Running Unit Tests"
    cd "${PROJECT_ROOT}"
    pytest tests/unit/ -v
}

cmd_test_integration() {
    print_header "Running Integration Tests"
    cd "${PROJECT_ROOT}"
    pytest tests/integration/ -v -m "not blender"
}

cmd_test_explosion() {
    print_header "Running Explosion System Tests"
    cd "${PROJECT_ROOT}"
    pytest tests/explosions/ -v
}

cmd_test_blender() {
    print_header "Running Blender Tests (requires MCP server)"
    print_warning "Make sure Blender is running with MCP server connected!"
    cd "${PROJECT_ROOT}"
    pytest tests/ -v -m "blender"
}

cmd_test_coverage() {
    print_header "Running Tests with Coverage"
    cd "${PROJECT_ROOT}"
    pytest tests/ -v -m "not blender" --cov=scripts --cov=integrations --cov-report=html --cov-report=term
    print_success "Coverage report generated in htmlcov/index.html"
}

cmd_test_watch() {
    print_header "Running Tests in Watch Mode"
    cd "${PROJECT_ROOT}"
    pytest-watch tests/ -v -m "not blender"
}

# =============================================================================
# RENDERING - DADOSFERA PROJECT
# =============================================================================

cmd_render_dadosfera() {
    local quality="${1:-preview}"
    print_header "Rendering Dadosfera Project (${quality})"
    
    check_blender
    check_file "${DADOSFERA_BLEND}"
    
    print_info "Engine: CYCLES"
    print_info "Quality: ${quality}"
    print_info "Materials: Photorealistic"
    print_info "Frames: 1-240"
    
    ${BLENDER} "${DADOSFERA_BLEND}" \
        --background \
        --python "${RENDER_SERVICE}" \
        -- \
        --engine CYCLES \
        --quality "${quality}" \
        --materials photorealistic \
        --start 1 \
        --end 240
    
    print_success "Dadosfera render complete!"
}

cmd_render_dadosfera_eevee() {
    print_header "Rendering Dadosfera Project (EEVEE - Fast)"
    
    check_blender
    check_file "${DADOSFERA_BLEND}"
    
    print_info "Engine: EEVEE"
    print_info "Quality: preview"
    print_info "Materials: Photorealistic"
    
    ${BLENDER} "${DADOSFERA_BLEND}" \
        --background \
        --python "${RENDER_SERVICE}" \
        -- \
        --engine EEVEE \
        --quality preview \
        --materials photorealistic \
        --start 1 \
        --end 240
    
    print_success "Dadosfera EEVEE render complete!"
}

# =============================================================================
# RENDERING - EXPLOSION TEST PROJECT
# =============================================================================

cmd_render_explosion() {
    local quality="${1:-preview}"
    print_header "Rendering Explosion Test Scene (${quality})"
    
    check_blender
    check_file "${EXPLOSION_BLEND}"
    
    print_info "Engine: CYCLES"
    print_info "Quality: ${quality}"
    print_info "Materials: Default"
    print_info "Frames: 1-150"
    
    ${BLENDER} "${EXPLOSION_BLEND}" \
        --background \
        --python "${RENDER_SERVICE}" \
        -- \
        --engine CYCLES \
        --quality "${quality}" \
        --materials default \
        --start 1 \
        --end 150 \
        --output-name "explosion_test_${quality}"
    
    print_success "Explosion render complete!"
}

# =============================================================================
# RENDERING - BOTH PROJECTS
# =============================================================================

cmd_render_all() {
    local quality="${1:-preview}"
    print_header "Rendering All Projects (${quality})"
    
    print_info "Starting dadosfera render in background..."
    nohup bash -c "$(declare -f cmd_render_dadosfera print_header print_info print_success check_blender check_file); cmd_render_dadosfera ${quality}" > /tmp/dadosfera_render.log 2>&1 &
    local dadosfera_pid=$!
    
    print_info "Starting explosion render in background..."
    nohup bash -c "$(declare -f cmd_render_explosion print_header print_info print_success check_blender check_file); cmd_render_explosion ${quality}" > /tmp/explosion_render.log 2>&1 &
    local explosion_pid=$!
    
    print_success "Both renders started in background"
    print_info "Dadosfera PID: ${dadosfera_pid}"
    print_info "Explosion PID: ${explosion_pid}"
    print_info "Monitor with: make logs-tail"
}

# =============================================================================
# EXPLOSION SYSTEM
# =============================================================================

cmd_explosion_create() {
    print_header "Creating Explosion Showcase Video"
    ${PYTHON} "${SCRIPTS_DIR}/create_explosion_video.py" --quality production
}

cmd_explosion_analyze() {
    print_header "Analyzing Explosion Objects"
    ${PYTHON} "${SCRIPTS_DIR}/analyze_explosion_realism.py"
}

cmd_explosion_check() {
    print_header "Checking Explosion Configuration"
    ${PYTHON} "${SCRIPTS_DIR}/check_explosion_objects.py"
}

cmd_explosion_video() {
    local quality="${1:-preview}"
    print_header "Creating Explosion Video (${quality})"
    ${PYTHON} "${SCRIPTS_DIR}/create_explosion_video.py" --quality "${quality}"
}

# =============================================================================
# VIDEO ENCODING
# =============================================================================

cmd_encode_dadosfera() {
    print_header "Encoding Dadosfera Frames to Video"
    
    # Find the latest render directory
    local latest_render=$(ls -td "${PROJECTS_DIR}"/dadosfera/renders/*/ 2>/dev/null | head -1)
    
    if [ -z "${latest_render}" ]; then
        print_error "No render directory found"
        exit 1
    fi
    
    print_info "Encoding from: ${latest_render}"
    
    local output_video="${PROJECTS_DIR}/dadosfera/exports/dadosfera_$(date +%Y%m%d_%H%M).mp4"
    
    ffmpeg -y \
        -framerate 24 \
        -i "${latest_render}frame_%04d.png" \
        -c:v libx264 \
        -preset medium \
        -crf 18 \
        -pix_fmt yuv420p \
        -movflags +faststart \
        "${output_video}"
    
    print_success "Video encoded: ${output_video}"
}

cmd_encode_explosion() {
    print_header "Encoding Explosion Frames to Video"
    
    # Find the latest explosion render directory
    local latest_render=$(ls -td "${PROJECTS_DIR}"/dadosfera/renders/explosion_test_*/ 2>/dev/null | head -1)
    
    if [ -z "${latest_render}" ]; then
        print_error "No explosion render directory found"
        exit 1
    fi
    
    print_info "Encoding from: ${latest_render}"
    
    local output_video="${PROJECTS_DIR}/explosion-test/exports/explosion_test_$(date +%Y%m%d_%H%M).mp4"
    
    ffmpeg -y \
        -framerate 24 \
        -i "${latest_render}frame_%04d.png" \
        -c:v libx264 \
        -preset medium \
        -crf 18 \
        -pix_fmt yuv420p \
        -movflags +faststart \
        "${output_video}"
    
    print_success "Video encoded: ${output_video}"
}

# =============================================================================
# MONITORING
# =============================================================================

cmd_monitor_render() {
    print_header "Monitoring Render Progress"
    bash "${SCRIPTS_DIR}/monitor_render.sh"
}

cmd_check_render_progress() {
    print_header "Checking Render Progress"
    bash "${SCRIPTS_DIR}/check_render_progress.sh"
}

cmd_show_logs() {
    print_header "Recent Render Logs"
    
    if [ -d "${LOGS_DIR}" ]; then
        print_info "Latest log files:"
        ls -lht "${LOGS_DIR}"/render_*.log 2>/dev/null | head -5 || print_warning "No render logs found"
    else
        print_warning "Logs directory not found"
    fi
}

cmd_tail_logs() {
    print_header "Tailing Render Logs"
    
    local dadosfera_log="/tmp/dadosfera_render.log"
    local explosion_log="/tmp/explosion_render.log"
    
    if [ -f "${dadosfera_log}" ] && [ -f "${explosion_log}" ]; then
        print_info "Tailing both render logs..."
        tail -f "${dadosfera_log}" "${explosion_log}"
    elif [ -f "${dadosfera_log}" ]; then
        print_info "Tailing dadosfera render log..."
        tail -f "${dadosfera_log}"
    elif [ -f "${explosion_log}" ]; then
        print_info "Tailing explosion render log..."
        tail -f "${explosion_log}"
    else
        # Fall back to project logs directory
        local latest_log=$(ls -t "${LOGS_DIR}"/render_*.log 2>/dev/null | head -1)
        if [ -n "${latest_log}" ]; then
            print_info "Tailing latest log: ${latest_log}"
            tail -f "${latest_log}"
        else
            print_warning "No render logs found"
        fi
    fi
}

# =============================================================================
# INTEGRATIONS
# =============================================================================

cmd_integration() {
    local phase="${1:-basic}"
    print_header "Running Integration Phase: ${phase}"
    
    case "${phase}" in
        phase1)
            cd "${INTEGRATIONS_DIR}/phase1"
            ${PYTHON} main.py
            ;;
        phase2)
            cd "${INTEGRATIONS_DIR}/phase2"
            ${PYTHON} main.py
            ;;
        phase3)
            cd "${INTEGRATIONS_DIR}/phase3"
            ${PYTHON} main.py
            ;;
        phase4)
            cd "${INTEGRATIONS_DIR}/phase4"
            ${PYTHON} main.py
            ;;
        basic)
            cd "${INTEGRATIONS_DIR}/basic"
            ${PYTHON} main.py demo
            ;;
        *)
            print_error "Unknown integration phase: ${phase}"
            exit 1
            ;;
    esac
    
    print_success "Integration complete"
}

# =============================================================================
# CLEANUP
# =============================================================================

cmd_clean() {
    print_header "Cleaning Temporary Files"
    find "${PROJECT_ROOT}" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find "${PROJECT_ROOT}" -type f -name "*.pyc" -delete 2>/dev/null || true
    find "${PROJECT_ROOT}" -type f -name "*.pyo" -delete 2>/dev/null || true
    find "${PROJECT_ROOT}" -type f -name ".DS_Store" -delete 2>/dev/null || true
    print_success "Temporary files cleaned"
}

cmd_clean_logs() {
    print_header "Cleaning Old Logs"
    print_warning "This will delete logs older than 7 days"
    read -p "Continue? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        find "${LOGS_DIR}" -type f -name "*.log" -mtime +7 -delete 2>/dev/null || true
        find /tmp -type f -name "*_render.log" -mtime +7 -delete 2>/dev/null || true
        print_success "Old logs cleaned"
    else
        print_info "Cancelled"
    fi
}

cmd_clean_cache() {
    print_header "Cleaning Python Cache"
    cmd_clean
    rm -rf "${PROJECT_ROOT}/htmlcov" 2>/dev/null || true
    rm -f "${PROJECT_ROOT}/.coverage" 2>/dev/null || true
    rm -rf "${PROJECT_ROOT}/.pytest_cache" 2>/dev/null || true
    print_success "Cache cleaned"
}

cmd_clean_renders() {
    print_header "Cleaning Old Renders"
    print_error "WARNING: This will delete render files!"
    print_warning "Only renders older than 30 days will be deleted"
    read -p "Continue? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        find "${PROJECTS_DIR}/dadosfera/renders" -type d -mtime +30 -exec rm -rf {} + 2>/dev/null || true
        find "${PROJECTS_DIR}/explosion-test/renders" -type d -mtime +30 -exec rm -rf {} + 2>/dev/null || true
        print_success "Old renders cleaned"
    else
        print_info "Cancelled"
    fi
}

cmd_clean_all() {
    print_header "Cleaning Everything"
    cmd_clean
    cmd_clean_logs
    cmd_clean_cache
    print_success "All cleanup complete"
}

# =============================================================================
# DEVELOPMENT
# =============================================================================

cmd_lint() {
    print_header "Running Linters"
    
    if command -v ruff &> /dev/null; then
        print_info "Running ruff..."
        ruff check "${SCRIPTS_DIR}" "${INTEGRATIONS_DIR}"
    elif command -v flake8 &> /dev/null; then
        print_info "Running flake8..."
        flake8 "${SCRIPTS_DIR}" "${INTEGRATIONS_DIR}"
    else
        print_warning "No linter found. Install ruff or flake8"
    fi
}

cmd_format() {
    print_header "Formatting Python Code"
    
    if command -v black &> /dev/null; then
        black "${SCRIPTS_DIR}" "${INTEGRATIONS_DIR}"
        print_success "Code formatted with black"
    else
        print_warning "Black not installed. Run: pip install black"
    fi
}

cmd_generate_report() {
    print_header "Generating Project Report"
    ${PYTHON} "${SCRIPTS_DIR}/generate_report.py"
}

cmd_install_hooks() {
    print_header "Installing Git Hooks"
    bash "${SCRIPTS_DIR}/hooks/install.sh"
}

cmd_update_mcp() {
    print_header "Updating Blender MCP Submodule"
    cd "${PROJECT_ROOT}"
    git submodule update --remote blender-mcp
    print_success "MCP submodule updated"
}

# =============================================================================
# PROJECT INFO
# =============================================================================

cmd_status() {
    print_header "Project Status"
    
    # Check running renders
    print_info "Running Blender processes:"
    ps aux | grep -i blender | grep -v grep | grep -v blender-mcp || print_warning "No active renders"
    
    echo ""
    
    # Check recent renders with full paths
    print_info "Recent render outputs:"
    local dadosfera_renders="${PROJECT_ROOT}/projects/dadosfera/renders"
    if [ -d "${dadosfera_renders}" ]; then
        ls -lht "${dadosfera_renders}" 2>/dev/null | head -5 || true
    fi
    local explosion_renders="${PROJECT_ROOT}/projects/explosion-test/renders"
    if [ -d "${explosion_renders}" ]; then
        ls -lht "${explosion_renders}" 2>/dev/null | head -5 || true
    fi
    
    echo ""
    
    # Check logs
    print_info "Recent logs:"
    ls -lht "${LOGS_DIR}"/*.log 2>/dev/null | head -3 || print_warning "No recent logs"
    
    echo ""
    
    # Add recent exported videos
    print_info "Recent exported videos:"
    local dadosfera_exports="${PROJECT_ROOT}/projects/dadosfera/exports"
    if [ -d "${dadosfera_exports}" ]; then
        find "${dadosfera_exports}" -name "*.mp4" -mmin -1440 -ls 2>/dev/null | tail -5 || true
    fi
    local explosion_exports="${PROJECT_ROOT}/projects/explosion-test/exports"
    if [ -d "${explosion_exports}" ]; then
        find "${explosion_exports}" -name "*.mp4" -mmin -1440 -ls 2>/dev/null | tail -5 || true
    fi
}

cmd_version() {
    print_header "Version Information"
    
    print_info "Python version:"
    ${PYTHON} --version
    
    echo ""
    
    if [ -f "${BLENDER}" ]; then
        print_info "Blender version:"
        ${BLENDER} --version | head -1
    else
        print_warning "Blender not found"
    fi
    
    echo ""
    
    print_info "Project version: v1.0-alpha"
}

cmd_info() {
    print_header "Project Information"
    
    cmd_version
    
    echo ""
    
    print_info "Project: 3D-DDF with Blender MCP Integration"
    print_info "Root: ${PROJECT_ROOT}"
    
    echo ""
    
    print_info "Projects:"
    echo "  - Dadosfera: ${PROJECTS_DIR}/dadosfera"
    echo "  - Explosion Test: ${PROJECTS_DIR}/explosion-test"
    
    echo ""
    
    print_info "Documentation: ${PROJECT_ROOT}/docs"
    print_info "Tests: ${TESTS_DIR}"
    print_info "Scripts: ${SCRIPTS_DIR}"
}

# =============================================================================
# MAIN COMMAND DISPATCHER
# =============================================================================

main() {
    local command="${1:-help}"
    shift || true
    
    case "${command}" in
        # Setup & Validation
        check) cmd_check "$@" ;;
        validate) cmd_validate "$@" ;;
        validate-docs) cmd_validate_docs "$@" ;;
        validate-taxonomy) cmd_validate_taxonomy "$@" ;;
        validate-json) cmd_validate_json "$@" ;;
        validate-links) cmd_validate_links "$@" ;;
        
        # Testing
        test) cmd_test "$@" ;;
        test-unit) cmd_test_unit "$@" ;;
        test-integration) cmd_test_integration "$@" ;;
        test-explosion) cmd_test_explosion "$@" ;;
        test-blender) cmd_test_blender "$@" ;;
        test-coverage) cmd_test_coverage "$@" ;;
        test-watch) cmd_test_watch "$@" ;;
        
        # Rendering - Dadosfera
        render-dadosfera) cmd_render_dadosfera "$@" ;;
        render-dadosfera-eevee) cmd_render_dadosfera_eevee "$@" ;;
        
        # Rendering - Explosion
        render-explosion) cmd_render_explosion "$@" ;;
        
        # Rendering - All
        render-all) cmd_render_all "$@" ;;
        
        # Explosion System
        explosion-create) cmd_explosion_create "$@" ;;
        explosion-analyze) cmd_explosion_analyze "$@" ;;
        explosion-check) cmd_explosion_check "$@" ;;
        explosion-video) cmd_explosion_video "$@" ;;
        
        # Video Encoding
        encode-dadosfera) cmd_encode_dadosfera "$@" ;;
        encode-explosion) cmd_encode_explosion "$@" ;;
        
        # Monitoring
        monitor-render) cmd_monitor_render "$@" ;;
        check-render-progress) cmd_check_render_progress "$@" ;;
        show-logs) cmd_show_logs "$@" ;;
        tail-logs) cmd_tail_logs "$@" ;;
        
        # Integrations
        integration) cmd_integration "$@" ;;
        
        # Cleanup
        clean) cmd_clean "$@" ;;
        clean-logs) cmd_clean_logs "$@" ;;
        clean-cache) cmd_clean_cache "$@" ;;
        clean-renders) cmd_clean_renders "$@" ;;
        clean-all) cmd_clean_all "$@" ;;
        
        # Development
        lint) cmd_lint "$@" ;;
        format) cmd_format "$@" ;;
        generate-report) cmd_generate_report "$@" ;;
        install-hooks) cmd_install_hooks "$@" ;;
        update-mcp) cmd_update_mcp "$@" ;;
        
        # Project Info
        status) cmd_status "$@" ;;
        version) cmd_version "$@" ;;
        info) cmd_info "$@" ;;
        
        # Help
        help|*)
            print_error "Unknown command: ${command}"
            echo ""
            print_info "Usage: $0 <command> [args]"
            print_info "Run 'make help' to see all available commands"
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"


