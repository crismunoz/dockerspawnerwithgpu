import os

# Point DockerSpawner to Swarm instead of the local DockerEngine
os.environ["DOCKER_HOST"] = ":4000"
                
# We not use SSL   
c.JupyterHub.confirm_no_ssl = False
        
c.JupyterHub.hub_ip = #THE IP OF YOUR INTERNAL NETWORK
c.JupyterHub.port=9000

c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.DockerSpawner.image = 'jupyter/datascience-notebook:latest'
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/root/student'
c.DockerSpawner.notebook_dir=notebook_dir
c.DockerSpawner.remove_containers = True
c.DockerSpawner.cmd='/usr/local/bin/start-singleuser.sh'
c.DockerSpawner.environment = {
'GRANT_SUDO': '1', 'NVIDIA_VISIBLE_DEVICES':'all',
}

c.Spawner.mem_limit = '5G'
c.Spawner.cpu_limit = 3.0

c.DockerSpawner.use_internal_ip = False

c.DockerSpawner.extra_host_config = {'runtime':'nvidia'}

c.DockerSpawner.volumes = { '/home/user/class/dl/jupyterhub-user-{username}': {'bind':'/root/student', 'mode':'rw'},\
			 '/export/share':{'bind':'/share','mode':'rw' },\
			 '/home/user/class/dl/keras':{'bind':'/root/.keras','mode':'rw'}}

c.DockerSpawner.container_ip = "0.0.0.0"


from tornado import gen
from jupyterhub.auth import Authenticator

the_password = 'ica123!'
class DummyAuthenticator(Authenticator):
    @gen.coroutine
    def authenticate(self, handler, data):
        if data['password'] == the_password:
            return data['username']

c.JupyterHub.authenticator_class = DummyAuthenticator

