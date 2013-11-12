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
import psycopg2
from unipath import Path
from celery import task
from .extralib.imageanalisys import main2d
from .extralib.hadapi.hadapi import hadoopHandler
from nanothings.settings import DEFAULT_HTTP_OUTPUT



@task()
def add(x, y):
    import time
    time.sleep(600)
    return x + y


@task()
def process_int(url_list1, url_list2, url_list3):
    import time
    time.sleep(60)
    out = [url_list1, url_list2, url_list3]
    return out


@task()
def minus(x, y):
    import time
    time.sleep(15)
    return x - y


@task()
def run_3d_analisys(conditions, outdir, cond_lbl_list,slice_label, chan_lbl_list,mask_index, molecule_index,mask_channel, molecule_channel):
    main2d.main_api(conditions, outdir, cond_lbl_list, slice_label, chan_lbl_list, mask_index, molecule_index,
                    mask_channel, molecule_channel,
                    mask_otsu= True, mask_fillholes= True, molecule_otsu= False, molecule_fillholes= False, single_object_analysis = False)

    dir = str(Path(outdir).name)
    return DEFAULT_HTTP_OUTPUT + "&path=/" + dir

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
    conn =  psycopg2.connect("dbname=wvtestmi user=postgres password=postgres host=geopg")
    cur = conn.cursor()
    cur.execute("select correlation_networks('http://192.168.205.138:8080/wang11synergy_pathways.csv','http://192.168.205.138:8080/wang11synergy_data.csv', 4910, 0.9);")
    res = cur.fetchone()

    dir = str(Path(res[0]).name)
    return 'http://192.168.205.10/owncloud/public.php?service=files&t=480d93ee44956ac9e26efc1d3321449e&path=/' + dir


@task()
def process_hadoop(int1, int2, int3):
    hd = hadoopHandler("pc05","userhadoop","user")
    hd.pheno_run("~/input12.txt","~/output12")

    return "OK"
