/*
 * (C) 2018 The University of Chicago
 * 
 * See COPYRIGHT in top-level directory.
 */
#define BOOST_NO_AUTO_PTR
#include <boost/python.hpp>
#include <boost/python/return_opaque_pointer.hpp>
#include <boost/python/handle.hpp>
#include <boost/python/enum.hpp>
#include <boost/python/def.hpp>
#include <boost/python/module.hpp>
#include <boost/python/return_value_policy.hpp>
#include <string>
#include <vector>
#include <cstring>
#include <iostream>
#include <margo.h>
#include <mobject-server.h>
#include <sdskv-server.h>
#include <sdskv-client.h>
#include <bake-client.h>

BOOST_PYTHON_OPAQUE_SPECIALIZED_TYPE_ID(margo_instance)
BOOST_PYTHON_OPAQUE_SPECIALIZED_TYPE_ID(mobject_server_context)
BOOST_PYTHON_OPAQUE_SPECIALIZED_TYPE_ID(sdskv_server_context_t)
BOOST_PYTHON_OPAQUE_SPECIALIZED_TYPE_ID(bake_provider_handle)
BOOST_PYTHON_OPAQUE_SPECIALIZED_TYPE_ID(sdskv_provider_handle)

namespace bpl = boost::python;

static mobject_provider_t pymobject_provider_register(
        margo_instance_id mid, uint8_t mplex_id,
        bake_provider_handle_t bake_ph,
        sdskv_provider_handle_t sdskv_ph,
        const std::string& cluster_file)
{
    mobject_provider_t provider;
    int ret = mobject_provider_register(mid, mplex_id, MOBJECT_ABT_POOL_DEFAULT, 
                                        bake_ph, sdskv_ph, cluster_file.c_str(),
                                        &provider);
    if(ret != 0) return NULL;
    else return provider;
}

BOOST_PYTHON_MODULE(_pymobjectserver)
{
#define ret_policy_opaque bpl::return_value_policy<bpl::return_opaque_pointer>()

    bpl::opaque<mobject_server_context>();
    bpl::def("register", &pymobject_provider_register, ret_policy_opaque);
    bpl::def("setup_sdskv_provider", &mobject_sdskv_provider_setup);

#undef ret_policy_opaque
}
