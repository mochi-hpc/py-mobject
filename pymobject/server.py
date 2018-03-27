# (C) 2018 The University of Chicago
# See COPYRIGHT in top-level directory.
import _pymobjectserver
import pymargo

def setup_sdskv_databases(kv_provider):
	_pymobjectserver.setup_sdskv_provider(kv_provider._provider)

class MobjectProvider(pymargo.Provider):

	def __init__(self, mid, mplex_id, bake_ph, sdskv_ph, ssg_group, cluster_file):
		super(MobjectProvider, self).__init__(mid, mplex_id)
		self._provider = _pymobjectserver.register(mid._mid, 
					mplex_id, bake_ph._ph,
					sdskv_ph._ph, ssg_group._gid, cluster_file)

