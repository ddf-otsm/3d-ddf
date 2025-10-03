# 3D-DDF Makefile
# Common operations for the 3D-DDF project with Blender MCP integration

.PHONY: help
.DEFAULT_GOAL := help

# Color output
YELLOW := \033[1;33m
GREEN := \033[1;32m
BLUE := \033[1;34m
RED := \033[1;31m
RESET := \033[0m

# Common variables
BLENDER := /Applications/Blender.app/Contents/MacOS/Blender
WORKFLOWS := ./workflows/run.sh

help: ## Show this help message
	@echo "$(GREEN)3D-DDF Makefile - Common Operations$(RESET)"
	@echo ""
	@echo "$(YELLOW)Usage:$(RESET) make [target]"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(BLUE)%-25s$(RESET) %s\n", $$1, $$2}'

# =============================================================================
# SETUP & VALIDATION
# =============================================================================

check: ## Check Blender installation and environment
	@$(WORKFLOWS) check

validate: ## Run all validation checks (docs, taxonomy, json, links)
	@$(WORKFLOWS) validate

validate-docs: ## Validate documentation files
	@$(WORKFLOWS) validate-docs

validate-taxonomy: ## Validate project taxonomy and structure
	@$(WORKFLOWS) validate-taxonomy

validate-json: ## Validate JSON configuration files
	@$(WORKFLOWS) validate-json

validate-links: ## Validate markdown links
	@$(WORKFLOWS) validate-links

# =============================================================================
# TESTING
# =============================================================================

test: ## Run all tests (excluding Blender tests)
	@$(WORKFLOWS) test

test-unit: ## Run unit tests only
	@$(WORKFLOWS) test-unit

test-integration: ## Run integration tests only
	@$(WORKFLOWS) test-integration

test-explosion: ## Run explosion system tests
	@$(WORKFLOWS) test-explosion

test-blender: ## Run tests requiring Blender (must have MCP server running)
	@$(WORKFLOWS) test-blender

test-coverage: ## Run tests with coverage report
	@$(WORKFLOWS) test-coverage

test-watch: ## Run tests in watch mode
	@$(WORKFLOWS) test-watch

# =============================================================================
# RENDERING - DADOSFERA PROJECT
# =============================================================================

render-dadosfera: ## Render dadosfera project (Cycles, preview quality)
	@$(WORKFLOWS) render-dadosfera preview

render-dadosfera-draft: ## Render dadosfera project (Cycles, draft quality - fast)
	@$(WORKFLOWS) render-dadosfera draft

render-dadosfera-production: ## Render dadosfera project (Cycles, production quality)
	@$(WORKFLOWS) render-dadosfera production

render-dadosfera-final: ## Render dadosfera project (Cycles, final quality - highest)
	@$(WORKFLOWS) render-dadosfera final

render-dadosfera-eevee: ## Render dadosfera project (EEVEE, preview quality - fastest)
	@$(WORKFLOWS) render-dadosfera-eevee

# =============================================================================
# RENDERING - EXPLOSION TEST PROJECT
# =============================================================================

render-explosion: ## Render explosion test scene (Cycles, preview quality)
	@$(WORKFLOWS) render-explosion preview

render-explosion-draft: ## Render explosion test scene (Cycles, draft quality - fast)
	@$(WORKFLOWS) render-explosion draft

render-explosion-production: ## Render explosion test scene (Cycles, production quality)
	@$(WORKFLOWS) render-explosion production

render-explosion-final: ## Render explosion test scene (Cycles, final quality - highest)
	@$(WORKFLOWS) render-explosion final

# =============================================================================
# RENDERING - BOTH PROJECTS
# =============================================================================

render-all: ## Render both dadosfera and explosion projects (preview quality)
	@$(WORKFLOWS) render-all preview

render-all-draft: ## Render both projects (draft quality - fast)
	@$(WORKFLOWS) render-all draft

render-all-production: ## Render both projects (production quality)
	@$(WORKFLOWS) render-all production

# =============================================================================
# EXPLOSION SYSTEM
# =============================================================================

explosion-create: ## Create explosion showcase video
	@$(WORKFLOWS) explosion-create

explosion-analyze: ## Analyze current explosion objects
	@$(WORKFLOWS) explosion-analyze

explosion-check: ## Check explosion configuration
	@$(WORKFLOWS) explosion-check

explosion-video: ## Create explosion video with specific quality (usage: make explosion-video QUALITY=production)
	@$(WORKFLOWS) explosion-video $(or $(QUALITY),preview)

# =============================================================================
# VIDEO ENCODING
# =============================================================================

encode-dadosfera: ## Encode dadosfera frames to video
	@$(WORKFLOWS) encode-dadosfera

encode-explosion: ## Encode explosion frames to video
	@$(WORKFLOWS) encode-explosion

# =============================================================================
# MONITORING
# =============================================================================

monitor-render: ## Monitor current render progress
	@$(WORKFLOWS) monitor-render

check-render-progress: ## Check render progress from logs
	@$(WORKFLOWS) check-render-progress

logs: ## Show recent render logs
	@$(WORKFLOWS) show-logs

logs-tail: ## Tail render logs in real-time
	@$(WORKFLOWS) tail-logs

# =============================================================================
# INTEGRATIONS (3D Asset Platforms)
# =============================================================================

integration-phase1: ## Run Phase 1 integration (Free platforms)
	@$(WORKFLOWS) integration phase1

integration-phase2: ## Run Phase 2 integration (Free with registration)
	@$(WORKFLOWS) integration phase2

integration-phase3: ## Run Phase 3 integration (Professional platforms)
	@$(WORKFLOWS) integration phase3

integration-phase4: ## Run Phase 4 integration (Enterprise platforms)
	@$(WORKFLOWS) integration phase4

integration-basic: ## Run basic integration demo (no auth required)
	@$(WORKFLOWS) integration basic

# =============================================================================
# CLEANUP
# =============================================================================

clean: ## Clean temporary files and caches
	@$(WORKFLOWS) clean

clean-logs: ## Clean old log files
	@$(WORKFLOWS) clean-logs

clean-cache: ## Clean Python cache files
	@$(WORKFLOWS) clean-cache

clean-renders: ## Clean old render outputs (WARNING: will delete render files)
	@$(WORKFLOWS) clean-renders

clean-all: ## Clean everything (logs, cache, renders)
	@$(WORKFLOWS) clean-all

# =============================================================================
# DEVELOPMENT
# =============================================================================

lint: ## Run linters on Python code
	@$(WORKFLOWS) lint

format: ## Format Python code with black
	@$(WORKFLOWS) format

report: ## Generate project report
	@$(WORKFLOWS) generate-report

install-hooks: ## Install git hooks
	@$(WORKFLOWS) install-hooks

update-mcp: ## Update Blender MCP submodule
	@$(WORKFLOWS) update-mcp

# =============================================================================
# PROJECT INFO
# =============================================================================

status: ## Show project status
	@$(WORKFLOWS) status

version: ## Show project and Blender versions
	@$(WORKFLOWS) version

info: ## Show detailed project information
	@$(WORKFLOWS) info


