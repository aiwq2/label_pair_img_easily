import tkinter as tk
import os
from PIL import Image, ImageTk
import random

class face():
    save_file=''
    id2img_path=dict()
    
    def __init__(self,master,id,screenwidth,screenheight,is_pair):
        self.screenwidth=screenwidth
        self.screenheight=screenheight
        self.id=id
        self.id_count=len(self.id2img_path)
        self.master = master
        self.is_pair=is_pair
        # 配置多个Frame
        self.face = tk.Frame(self.master,)
        self.img_frame=tk.Frame(self.face)
        self.choose_frame=tk.Frame(self.face)
        self.info_frame=tk.Frame(self.face)
        self.spinbox = None
        # 根据id获取图片路径
        if is_pair:
            self.img_path1=self.id2img_path[id][0]
            self.img_path2=self.id2img_path[id][1]
        else:
            self.img_path= self.id2img_path[id]
        self.values=self.get_values()
        self.text_in_button=self.text_config()
        self.set_info()
        self.jump_to_images()
        
        if id!=0:
            btn_back = tk.Button(self.info_frame,text=f'上一{self.text_in_button}图片',command=self.back,width=20,height=10).grid(row=0,column=0,padx=20, pady=20,sticky='w')
        if id!=self.id_count-1:
            btn_next = tk.Button(self.info_frame,text=f'下一{self.text_in_button}图片',command=self.next,width=20,height=10).grid(row=0,column=1,padx=5, pady=5,sticky='e')
        if self.is_pair:
            img1,img2=self.img_deal()
            self.choose(img1,img2)
        else:
            img=self.img_deal()
            self.choose(img)
        self.img_frame.grid(row=0,column=0)
        self.choose_frame.grid(row=1,column=0)
        self.info_frame.grid(row=2,column=0)
        self.face.pack()
    
    def text_config(self):
        if self.is_pair:
            return '对'
        else:
            return '张'

    def set_info(self):
        if self.is_pair:
            tk.Label(self.info_frame,text='第%d/%d%s图片'%(self.id+1,self.id_count,self.text_in_button)).grid(row=1,column=0,columnspan=2,padx=5, pady=5)
        else:
            tk.Label(self.info_frame,text='第%d/%d%s图片'%(self.id+1,self.id_count,self.text_in_button)).grid(row=1,column=0,columnspan=2,padx=5, pady=5)

    # 上一对图片
    def back(self):
        self.face.destroy()
        self.save_values()
        face(self.master,self.id-1,self.screenwidth,self.screenheight,self.is_pair)

    # 下一对图片
    def next(self):
        self.face.destroy()
        self.save_values()
        face(self.master,self.id+1,self.screenwidth,self.screenheight,self.is_pair)
    
    # 将值写入log文件，方便下次读取
    def save_values(self):
        self.values[self.id]=self.v.get()
        with open(self.save_file,'w') as f:
            for value in self.values:
                f.write(str(value)+'\n')

    # 从log文件中读取值
    def get_values(self):
        values=[]
        if os.path.exists(self.save_file):
            with open(self.save_file,'r') as f:
                for line in f.readlines():
                    values.append(int(line.strip()))
            return values
        else:
            return [-2]*self.id_count
    
    # 图片处理
    def img_deal(self): 
        if self.is_pair:
            img1 = Image.open(self.img_path1)
            scale_factor=self.get_scale_factor(img1)
            img1.thumbnail((int(img1.width * scale_factor), int(img1.height * scale_factor)))
            img2 = Image.open(self.img_path2)
            scale_factor=self.get_scale_factor(img2)
            img2.thumbnail((int(img2.width * scale_factor), int(img2.height * scale_factor)))
            return img1,img2
        else:
            img = Image.open(self.img_path)
            scale_factor=self.get_scale_factor(img)
            img.thumbnail((int(img.width * scale_factor), int(img.height * scale_factor)))
            return img

    
    # 获取缩放因子，使图片适应屏幕
    def get_scale_factor(self,img):
        width, height = img.size
        scale_factor = min(0.5*self.screenwidth / width, 0.5*self.screenheight / height)
        return scale_factor
    
    # 选择哪张图片更模糊
    def choose(self,*img_list):
        # IntVar() 用于处理整数类型的变量
        self.v = tk.IntVar()
        # 根据单选按钮的 value 值来选择相应的选项
        self.v.set(self.values[self.id])
        if self.is_pair:
            assert len(img_list)==2 , 'img_list长度应为2'
        else:
            assert len(img_list)==1 , 'img_list长度应为1'

        if self.is_pair:
            self.tkimg1 = ImageTk.PhotoImage(img_list[0])
            tk.Label(self.img_frame,image=self.tkimg1).grid(row=0,column=0)
            self.tkimg2=ImageTk.PhotoImage(img_list[1])
            tk.Label(self.img_frame,image=self.tkimg2).grid(row=0,column=1)
            # button2=tk.Button(text='more blur',width=10,height=5,command=more_blur2).grid(row=1,column=1,padx=5, pady=5)
            tk.Radiobutton(self.choose_frame, text="第1张更模糊", variable=self.v, value=-1,indicatoron = False).grid(row=0,column=0,padx=5, pady=5)
            tk.Radiobutton(self.choose_frame, text="清晰度相同", variable=self.v, value=0,indicatoron = False).grid(row=0,column=1,padx=5, pady=5)
            tk.Radiobutton(self.choose_frame, text="第2张更模糊", variable=self.v, value=1,indicatoron = False).grid(row=0,column=2,padx=5, pady=5)
        else:
            self.tkimg = ImageTk.PhotoImage(img_list[0])
            tk.Label(self.img_frame,image=self.tkimg).grid(row=0,column=0)
            tk.Radiobutton(self.choose_frame, text="模糊", variable=self.v, value=1,indicatoron = False).grid(row=0,column=0,padx=5, pady=5)
            tk.Radiobutton(self.choose_frame, text="不模糊", variable=self.v, value=0,indicatoron = False).grid(row=0,column=1,padx=5, pady=5)
    
    # 设置spinbox用于直接跳转图片
    def jump_to_images(self):
        def get_spinbox():
            value=self.spinbox.get()
            if value.isdigit() and int(value)<=self.id_count and int(value)>0:
                self.face.destroy()
                self.save_values()
                face(self.master,int(value)-1,self.screenwidth,self.screenheight,self.is_pair)
        self.spinbox = tk.Spinbox(self.info_frame,from_=1,to=self.id_count, increment=10,width = 15,bg='#9BCD9B')
        self.spinbox.grid(row=2,column=1,padx=5, pady=5,sticky='w')
        tk.Button(self.info_frame,text='跳转到图片id:',command=get_spinbox).grid(row=2,column=0,padx=5, pady=5,sticky='e')
        
        



def use_tkinter(img_dict,save_file,is_pair):
    root_window=tk.Tk()
    root_window.title('请判断哪幅图片更加模糊')
    # 窗口居中，获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
    width = 1000
    height = 1000
    screenwidth = root_window.winfo_screenwidth()
    screenheight = root_window.winfo_screenheight()
    size_geo = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)
    root_window.geometry(size_geo)

    face.id2img_path=img_dict
    face.save_file=save_file
    face(root_window,0,screenwidth,screenheight,is_pair)
    # button_quit=tk.Button(root_window,text="关闭",command=root_window.quit)
    # button_quit.grid(row=4)




    tk.mainloop()
    

# 将img_root_path下的图片两两配对，返回配对列表
def init_img_pair(img_pair_save_path='image_pair.txt',img_root_path='editor',img_start_index=0,img_nums=-1):
    if img_nums==-1:
        img_list=os.listdir(img_root_path)[img_start_index:]
    else:
        img_list=os.listdir(img_root_path)[img_start_index:img_start_index+img_nums]
    img_pair=[]
    random.seed(42)
    random.shuffle(img_list)
    last_pair=img_list.copy()

    # 
    while len(last_pair)>10:
        print(len(last_pair))
        img_deal=[]
        length_pair=len(last_pair)
        # 将最后一个图片和前面的图片配对
        if length_pair%2==1:
            if last_pair!=img_list:
                # 这里为[0][0]是自己定的，也可以选择[0][1]
                img_deal.append([last_pair[0][0],last_pair[length_pair-1][0]])
            else:
                img_deal.append([last_pair[0],last_pair[length_pair-1]])
            length_pair-=1
        for i in range(0,length_pair,2):
            if last_pair!=img_list:
                img_deal.append([last_pair[i][0],last_pair[i+1][0]])
            else:
                img_deal.append([img_list[i],img_list[i+1]])
        img_pair.extend(img_deal)
        last_pair=img_deal.copy()

    with open(img_pair_save_path,'w') as f:
        for pair in img_pair:
            f.write(pair[0]+','+pair[1]+'\n')

def init_img(img_name_save_path,img_root_path):
    with open(img_name_save_path,'w') as f:
        for img in os.listdir(img_root_path):
            f.write(img+'\n')

def get_img_dict(img_name_save_path,img_root_path):
    index_to_img_ditct={}
    with open(img_name_save_path,'r') as f:
        for index,line in enumerate(f.readlines()):
            index_to_img_ditct[index]=os.path.join(img_root_path,line.strip())
    return index_to_img_ditct

def get_img_pair_dict(img_name_save_path='image_pair.txt',img_root_path='editor'):
    img_pair_dict={}
    with open(img_name_save_path,'r') as f:
        for index,line in enumerate(f.readlines()):
            img_pair_dict[index]=[os.path.join(img_root_path,line.strip().split(',')[0]),os.path.join(img_root_path,line.strip().split(',')[1])]
    return img_pair_dict

def merge_imagepair_record(img_name_save_path,save_file,merge_path):

    with open(merge_path,'w') as f:
        with open(save_file,'r') as f1:
            with open(img_name_save_path,'r') as f2:
                for line1,line2 in zip(f1.readlines(),f2.readlines()):
                    f.write(line2.strip()+','+line1.strip()+'\n')


if __name__=='__main__':

    # 判断我们要在界面中看到的是否为一对图片
    is_pair=False

    # 参数调整部分,主要是图片的起始index和数量，以及文件名的前缀file_prefix用来做标识
    img_start_index=0
    img_nums=4000
    editor_name='zhangsan'
    edit_range=str(img_start_index)+'-'+str(img_start_index+img_nums)
    file_prefix='-'.join([editor_name,edit_range])+'-'
    # file_prefix的最终格式即为{editor_name}-{img_start_index}-{img_start_index+img_nums}-

    # 图片路径
    img_root_path='url_100000/img_nums4000'

    # 三个文件分别放置图片名字，打标签过程中的中间结果，最终结果
    img_name_save_path=file_prefix+'image_new.txt'
    save_file=file_prefix+'record.log'
    merge_path=file_prefix+'label.txt'

    # 初始化图片id到图片路径的映射，方便后续在图形界面对图片的调用
    if is_pair:
        if not os.path.exists(img_name_save_path):
            init_img_pair(img_name_save_path,img_root_path,img_start_index,img_nums)
        img_dict=get_img_pair_dict(img_name_save_path,img_root_path)
    else:
        if not os.path.exists(img_name_save_path):
            init_img(img_name_save_path,img_root_path)
        img_dict=get_img_dict(img_name_save_path,img_root_path)
    
    # 进入前端界面
    use_tkinter(img_dict,save_file,is_pair)
    # 将图片名字和中间结果合并得到最终结果
    merge_imagepair_record(img_name_save_path,save_file,merge_path)

