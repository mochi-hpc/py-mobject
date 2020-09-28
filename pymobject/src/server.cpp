/*
 * (C) 2018 The University of Chicago
 * 
 * See COPYRIGHT in top-level directory.
 */
#include <pybind11/pybind11.h>
#include <string>
#include <vector>
#include <cstring>
#include <iostream>
#include <margo.h>
#include <mobject-server.h>
#include <sdskv-server.h>
#include <sdskv-client.h>
#include <bake-client.h>
#include <ssg.h>

namespace py11 = pybind11;

typedef py11::capsule pymargo_instance_id;
typedef py11::capsule pymobject_provider_t;
typedef py11::capsule pysdskv_provider_t;
typedef py11::capsule pysdskv_provider_handle_t;
typedef py11::capsule pybake_provider_handle_t;
typedef ssg_group_id_t pyssg_group_id_t;

#define MID2CAPSULE(__mid)       py11::capsule((void*)(__mid),   "margo_instance_id", nullptr)
#define MOBJECTPR2CAPSULE(__mpr) py11::capsule((void*)(__mpr),   "mobject_provider_t", nullptr)
#define SDSKVPR2CAPSULE(__pr)    py11::capsule((void*)(__pr),    "sdskv_provider_t", nullptr)
#define SDSKVPH2CAPSULE(__ph)    py11::capsule((void*)(__ph),    "sdskv_provider_handle_t", nullptr)
#define BAKEPH2CAPSULE(__pr)     py11::capsule((void*)(__pr),    "bake_provider_handle_t", nullptr)

static pymobject_provider_t pymobject_provider_register(
        pymargo_instance_id mid, uint8_t provider_id,
        pybake_provider_handle_t bake_ph,
        pysdskv_provider_handle_t sdskv_ph,
        pyssg_group_id_t gid,
        const std::string& cluster_file)
{
    mobject_provider_t provider;
    int ret = mobject_provider_register(mid, provider_id, MOBJECT_ABT_POOL_DEFAULT, 
                                        bake_ph, sdskv_ph, gid, cluster_file.c_str(),
                                        &provider);
    if(ret != 0) return py11::none();
    else return MOBJECTPR2CAPSULE(provider);
}

PYBIND11_MODULE(_pymobjectserver, m)
{
    m.def("register", &pymobject_provider_register);
    m.def("setup_sdskv_provider", [](pysdskv_provider_t pr, const std::string& path, sdskv_db_type_t backend) {
            return mobject_sdskv_provider_setup(pr, path.c_str(), backend); });
}
