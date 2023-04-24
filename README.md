# pwcPythonYearReport

1.getDataExcel.py 用于下载深沪京板块公司包含年报的PDF下载链接的Excel
  巨潮网单次查询最多显示100页，根据时间段来分别查询，得到多个Excel文件，手动合并即可（ctrl+C、ctrl+V）
  url为深沪京，其他主板上的公司直接替换url即可
  
2.downloadPDF.py 用于根据上一步得到的Excel来下载PDF

3.convertTxt.py 用于将PDF文件转为TXT，并且从中截取包含‘管理层讨论与分析’‘公司治理’的页面的段落