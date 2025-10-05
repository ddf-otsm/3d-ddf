import jenkins.model.*
import hudson.model.*
import hudson.plugins.git.*
import hudson.plugins.git.extensions.*
import org.jenkinsci.plugins.workflow.job.WorkflowJob
import org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition

def jenkins = Jenkins.instance

// Create pipeline job
def job = jenkins.createProject(WorkflowJob, '3d-ddf-validation')
job.setDescription('3D-DDF Validation Pipeline')

// Configure Git SCM
def gitSCM = new GitSCM(
    Collections.singletonList(new UserRemoteConfig('https://github.com/ddf-otsm/3d-ddf.git', null, null, null)),
    Collections.singletonList(new BranchSpec('*/main')),
    false, Collections.emptyList(),
    null, null, Collections.emptyList()
)

// Configure pipeline definition
def flowDefinition = new CpsScmFlowDefinition(gitSCM, 'Jenkinsfile')
flowDefinition.setLightweight(true)
job.setDefinition(flowDefinition)

// Save the job
job.save()

println "Created job: 3d-ddf-validation"
