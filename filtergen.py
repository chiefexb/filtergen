#!/usr/bin/python
#coding: utf8
import sys
from os import *
from lxml import etree
from cStringIO import StringIO
import fdb
def main():
 qt="'"
 if len(sys.argv)<=5:
  print ("getfromint: нехватает параметров\nИспользование: getfromint ХОСТ ИМЯ_БД ПОЛЬЗОВАТЕЛЬ ПАРОЛЬ ПАПКА [НОМЕР КАТЕГОРИИ]")
  sys.exit(2)
 print sys.argv[1]
#Открытие файла конфигурации
 try:
  hostname=(sys.argv[1])
 except Exception,e:
  print e
  sys.exit(2) 
 try:
  database=(sys.argv[2])
 except Exception,e:
  print e
  sys.exit(2)
 try:
  username=(sys.argv[3])
 except Exception,e:
  print e
  sys.exit(2)
 try:
  password=(sys.argv[4])
 except Exception,e:
  print e
  sys.exit(2)
 concodepage='WIN1251'
 # hostname='localhost'
 # database='ncore-fssp'
 try:
  con = fdb.connect (host=hostname, database=database, user=username,  password=password,charset=concodepage) 
 except   Exception, e:
  print("Ошибка при открытии базы данных:\n"+str(e))
  sys.exit(2)
 cur = con.cursor()
 try:
  input_path=(sys.argv[5])
 except Exception,e:
  print e
  sys.exit(2)
#Цикл
 for ff in listdir(input_path):
  print "File:",ff
  try:
   parid=(sys.argv[6])
  except Exception,e:
   print e
   sys.exit(2)
  f=file(input_path+ff)
  xml = etree.parse(f)
  xmlroot=xml.getroot()
  flt=xmlroot.find('CustomSqlFilter')
  SqlFilterName=flt.attrib['SqlFilterName']
  SqlJoinPart=flt.attrib['SqlJoinPart']
  SqlWherePart=flt.attrib['SqlWherePart']
  print flt.attrib['SqlWherePart']
  SqlFilterDescription=flt.attrib['SqlFilterDescription']
  ObjectName=flt.attrib['ObjectName']
  genidsql='select gen_id (seq_custom_sql_filter,1) from rdb$database'
  sql='INSERT INTO CUSTOM_SQL_FILTER (ID, OBJECT_NAME, SQL_FILTER_NAME, SQL_JOIN_PART, SQL_WHERE_PART, SQL_FILTER_DESCRIPTION, IS_LIST_VISIBLE, IS_STAT_VISIBLE, IS_ANALYTICS_VISIBLE, PARENT_ID) VALUES (?,?,?,?,?,?,?,?,?,?)'
  print sql
  print SqlWherePart
  cur.execute(genidsql)
  r=cur.fetchall()
  genid=r[0][0]
  print genid
  cur.execute (sql,(genid, ObjectName,  (SqlFilterName)   ,(SqlJoinPart), (SqlWherePart),   SqlFilterDescription  , 1 , 1 , 1,parid))
  con.commit()
  f.close
 con.close()
if __name__ == "__main__":
    main()

