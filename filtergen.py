#!/usr/bin/python
#coding: utf8
import sys
from lxml import etree
from cStringIO import StringIO
import fdb
def main():
 qt="'"
 if len(sys.argv)<=1:
  print ("getfromint: нехватает параметров\nИспользование: getfromint ФАЙЛ_КОНФИГУРАЦИИ")
  sys.exit(2)
 print sys.argv[1]
#Открытие файла конфигурации
 try:
  f=file(sys.argv[1])
 except Exception,e:
  print e
  sys.exit(2)
 try:
  parid=(sys.argv[2])
 except Exception,e:
  print e
  sys.exit(2)
 xml = etree.parse(f)
 xmlroot=xml.getroot()
 flt=xmlroot.find('CustomSqlFilter')
 SqlFilterName=flt.attrib['SqlFilterName']
#.encode('CP1251')
 print "1"
 SqlJoinPart=flt.attrib['SqlJoinPart']
#.encode('CP1251')
 #print 
 SqlWherePart=flt.attrib['SqlWherePart']
#.encode('CP1251')
 print flt.attrib['SqlWherePart']
 SqlFilterDescription=flt.attrib['SqlFilterDescription']
#.encode('CP1251')
 ObjectName=flt.attrib['ObjectName']
 genidsql='select gen_id (seq_custom_sql_filter,1) from rdb$database'
 sql='INSERT INTO CUSTOM_SQL_FILTER (ID, OBJECT_NAME, SQL_FILTER_NAME, SQL_JOIN_PART, SQL_WHERE_PART, SQL_FILTER_DESCRIPTION, IS_LIST_VISIBLE, IS_STAT_VISIBLE, IS_ANALYTICS_VISIBLE, PARENT_ID) VALUES (?,?,?,?,?,?,?,?,?,?)'
 #sql=sql+genid+", "+qt+"doc_ip_doc"+qt+", "
#+qt + SqlFilterName + qt+", "+qt+SqlJoinPart+qt+ " , "+qt+SqlWherePart+ qt+", "+qt+SqlFilterDescription+qt+", 1, 1, 1,"+parid+" );"
#17121000000120, 'doc_ip_doc', '111111', NULL, NULL, NULL, 1, 1, 1, 17121000000085);' 
 
 username='SYSDBA'
 password='masterkey'
 concodepage='WIN1251'
 hostname='localhost'
 database='ncore-fssp'
 try:
  con = fdb.connect (host=hostname, database=database, user=username, password=password,charset=concodepage)
 except  Exception, e:
  print("Ошибка при открытии базы данных:\n"+str(e))
  sys.exit(2)
 cur = con.cursor()
 print sql
 print SqlWherePart
 cur.execute(genidsql)
 r=cur.fetchall()
 genid=r[0][0]
 print genid
#                   ID,    OBJECT_NAME, SQL_FILTER_NAME, SQL_JOIN_PART,SQL_WHERE_PART, SQL_FILTER_DESCRIPTION, IS_LIST_VISIBLE, IS_STAT_VISIBLE, IS_ANALYTICS_VISIBLE, PARENT_ID) VALUES (?)
 cur.execute (sql,(genid, ObjectName,  (SqlFilterName)   ,(SqlJoinPart), (SqlWherePart),   SqlFilterDescription  , 1 , 1 , 1,parid))
#(sql.decode('UTF-8').encode(concodepage))
 con.commit()
 con.close()
 f.close()
if __name__ == "__main__":
    main()

