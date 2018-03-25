# (C) 2018 The University of Chicago
# See COPYRIGHT in top-level directory.

# Importing MPI from mpi4py triggers a call to MPI_Init,
# which is needed by the Mobject provider.
from mpi4py           import MPI
from pymargo          import MargoInstance
from pysdskv.server   import SDSKVProvider
from pysdskv.client   import SDSKVClient
import pybake.server
from pybake.server    import BakeProvider
from pybake.client    import BakeClient
import pyssg
import pymobject.server
from pymobject.server import MobjectProvider

print "=== Initializing Margo"
mid = MargoInstance('tcp')
print "=== Enabling remote shutdown"
mid.enable_remote_shutdown()

print "=== Initializing SSG"
pyssg.init(mid)

this_addr = mid.addr()

pool_name = "/dev/shm/mobject.dat"
pool_size = 10*1024*1024
print "=== Creating a Bake pool ("+pool_name+" of size "+str(pool_size)+")"
pybake.server.make_pool(pool_name, pool_size, 0664)

print "=== Initializing the Bake provider"
bake_provider  = BakeProvider(mid, 1)
print "=== Adding target pool to Bake provider"
bake_provider.add_storage_target(pool_name)

print "=== Initializing the SDS-KeyVal provider"
sdskv_provider = SDSKVProvider(mid, 1)
print "=== Setting up SDS-KeyVal databases required by Mobject"
pymobject.server.setup_sdskv_databases(sdskv_provider)

print "=== Creating Bake client"
bake_client  = BakeClient(mid)
print "=== Creating SDS-KeyVak client"
sdskv_client = SDSKVClient(mid)

print "=== Creating Bake provider handle"
bake_provider_handle  = bake_client.create_provider_handle(this_addr, 1)
print "=== Creating SDS-KeyVal provider handle"
sdskv_provider_handle = sdskv_client.create_provider_handle(this_addr, 1)

cluster_file = "mobject-cluster.txt"
print "=== Initializing Mobject provider (cluster file is "+cluster_file+")"
mobject_provider = MobjectProvider(mid, 1, bake_provider_handle,
				sdskv_provider_handle, "cluster_file.txt")

print "=== Server running at "+str(this_addr)

mid.wait_for_finalize()
