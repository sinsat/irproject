#! /usr/bin/python -tt
import bs4
import sys
import os
import json
import copy

def merge(directory,mfile_name):
	dict1={}
	filelist = os.listdir(directory)
	for file1 in filelist:
		f=open(directory+'/'+file1,'r')
		s=f.read()
		t=json.loads(s)
		f.close()
		for k in sorted(t.keys()):
			dict1[k]=t[k]
		dict2={}
		for k in sorted(dict1.keys()):
			dict2[k]=dict1[k]
		dict1=dict2
		dict2={}
	final=open(mfile_name,'w')
	json.dump(dict1,final)
	final.close()
	for file1 in filelist:
		os.remove(directory+'/'+file1)

def main():
	dict1={}
	dict2={}
	dict3={}
	filelist=os.listdir("../data/careercup/database")
	fileno=1
	ofno=0
	if not os.path.exists('./temp1'):
		os.makedirs('./temp1')
	if not os.path.exists('./temp2'):
		os.makedirs('./temp2')
	if not os.path.exists('./temp3'):
		os.makedirs('./temp3')
	for file1 in filelist:
		print file1
		filename="../data/careercup/database/"+file1
		f=open(filename)
		html=f.read()
		f.close()
		soup=bs4.BeautifulSoup(html)
		tmp=soup.body
		if tmp==None:
			continue
		tmp=tmp.find('span',attrs={'class':'tags'})
		if tmp==None:
			continue
		tmp=tmp.find_all('a')
		#dict1[file1]=tmp.text
		tags=[]
		dict1[file1]=tags	
		if len(tmp)<=2:
			print 'c...'
			continue
		dict2[file1]=tmp[0].text
		dict3[file1]=tmp[1].text
		tmp=tmp[2:]
		for x in tmp:
			l=x.contents[0]
			#print l
			m=l[:]
			#m=copy.deepcopy(l)
			tags.append(l)
		soup=None
		fileno=fileno+1
		if fileno > 100:
			ofno=ofno+1
			outfile=open('./temp1/'+'tag_data'+str(ofno)+'.txt','w')
			json.dump(dict1,outfile)
			outfile.close()
			outfile=open('./temp2/'+'company_data'+str(ofno)+'.txt','w')
			json.dump(dict2,outfile)
			outfile.close()
			outfile=open('./temp3/'+'position_data'+str(ofno)+'.txt','w')
			json.dump(dict3,outfile)
			outfile.close()
			fileno=1
			dict1={}
			dict2={}
			dict3={}
	ofno+=1
	outfile=open('./temp1/'+'tag_data'+str(ofno)+'.txt','w')
	json.dump(dict1,outfile)
	outfile.close()
	outfile=open('./temp2/'+'company_data'+str(ofno)+'.txt','w')
	json.dump(dict2,outfile)
	outfile.close()
	outfile=open('./temp3/'+'position_data'+str(ofno)+'.txt','w')
	json.dump(dict3,outfile)
	outfile.close()	
	merge('./temp1','tag_data.txt')
	merge('./temp2','company_data.txt')
	merge('./temp3','position_data.txt')
	sys.exit(0)

if __name__ == '__main__':
	main()
