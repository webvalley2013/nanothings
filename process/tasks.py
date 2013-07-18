# This file is part of nanothings.
#
#     nanothings is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero GPL as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     nanothings is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero GPL for more details.
#
#     You should have received a copy of the GNU Affero GPL
#     along with nanothings.  If not, see <http://www.gnu.org/licenses/>.

# MODULES
from celery import task
from .extralib.imageanalisys import main2d
from .extralib.hadapi.hadapi import hadoopHandler
from nanothings.settings import DEFAULT_HTTP_OUTPUT
import psycopg2

@task()
def add(x, y):
    import time
    time.sleep(600)
    return x + y


@task()
def process_int(url_list1, url_list2, url_list3, int1):
    out = [url_list1, url_list2, url_list3, int1]
    return out


@task()
def minus(x, y):
    import time
    time.sleep(15)
    return x - y


@task()
def run_3d_analisys(cond, outpath, cond_lbl_list, slice_label, channel_labels):
    main2d.main_api(cond, outpath, cond_lbl_list, None, None, mask_index = 0, molecule_index = 1,
                    mask_channel= 1, molecule_channel= 0,
                    mask_otsu= True, mask_fillholes= True, molecule_otsu= False, molecule_fillholes= False)

    return DEFAULT_HTTP_OUTPUT + "&path=/" + outpath

# parameters["url_pathways"], parameters["url_data"], parameters["sel_pathways"], parameters["thr"]
@task()
def process_plr(url_pathways, url_data, sel_pathways, thr):
    # try:
        # cursor = connection.cursor()
    # cursor.execute(
    #     "select correlation_networks('http://192.168.205.138:8080/wang11synergy_pathways.csv','http://192.168.205.138:8080/wang11synergy_data.csv', 4910, 0.9)"
    # )
    #
    # except DatabaseError, e:
    #     transaction.rollback()
    #     msg = {
    #         "success": False,
    #         "message": str(e)
    #     }
    #     return HttpResponseBadRequest(json.dumps(msg))
    conn =  psycopg2.connect("dbname=wvtestmi user=postgres password=postgres host=192.168.205.10")
    cur = conn.cursor()
    cur.execute("select correlation_networks('http://192.168.205.138:8080/wang11synergy_pathways.csv','http://192.168.205.138:8080/wang11synergy_data.csv', 4910, 0.9);")
    res = cur.fetchone()

    return res[0]


@task()
def process_hadoop(int1, int2, int3):
    hd = hadoopHandler("pc05","userhadoop","user")
    hd.pheno_run("~/input12.txt","~/output12")

    return "OK"
