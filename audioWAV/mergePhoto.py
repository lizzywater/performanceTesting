__author__ = 'eleanor.cui'
# -*- coding: utf-8 -*-
import Image
import random
import ImageEnhance


def save_image(img,url,caseNum='new'):
    i = random.randint(0,100)
    img.save(url+caseNum+'_%d.png'%i)
    return (url+caseNum+'_%d.png'%i)

# Make img size to the same, add white border if the img is small
def make_img_to_same_size(img1,img2):
    x1,y1=img1.size
    x2,y2=img2.size
    if x1>=x2:
        x=x1
    else:
        x=x2
    if y1>=y2:
        y=y1
    else:
        y=y2
    nImg1=Image.new('RGBA',(x,y),"white")
    nImg1.paste(img1,(0,0,x1,y1))
    nImg2=Image.new('RGBA',(x,y),"white")
    nImg2.paste(img2,(0,0,x2,y2))
    # save_image(nImg1,'test/0TEST/draft')
    # save_image(nImg2,'test/0TEST/draft')
    return nImg1,nImg2

# calculate opacity status
def reduce_opacity(im,opacity):
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    #r,g,b,alpha=im.split()
    print "alpha info:"
    print alpha
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

##
# Using a mark layer to merge pics. Total opacity is 1 for mark and background.
# @opacity =0 get backgroundImg
# @opacity =1 get markImg
##
def composite_img_with_opacity(markImg,backgroundImg,opacity=1):
    markImg,backgroundImg=make_img_to_same_size(markImg,backgroundImg)
    if opacity<=1:
        if markImg.mode != 'RGBA':
            mark = markImg.convert('RGBA')
        else:
          mark = markImg.copy()
        alpha = mark.split()[3]
        #r,g,b,alpha=im.split()
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        mark.putalpha(alpha)
    return Image.composite(markImg,backgroundImg,mark)



##
# Total opacity is 1 for mark and background.
# @opacity =0 get markImg
# @opacity =1 get backgroundImg
##
def blend_img_with_opacity(markImg,backgroundImg,opacity=1):
    markImg,backgroundImg=make_img_to_same_size(markImg,backgroundImg)
    if opacity<1:
        mark=reduce_opacity(markImg,opacity)
    #backgroundImg.paste(markImg,None,mark)
    backgroundImg=Image.blend(markImg,backgroundImg,opacity)
    return backgroundImg





# Debug functions
def get_image_info(img):
    return img.format,img.size,img.mode


if __name__ == '__main__':
    # opacity[0,1]
    opacity = 1.0
    img1=Image.open('test/source/actual.JPG')
    img2=Image.open('test/source/expected.JPG')
    #imgNew=composite_img_with_opacity(img1,img2,opacity)
    #print get_image_info(imgNew)
    imgNew=blend_img_with_opacity(img1,img2,opacity)
    save_image(imgNew,'test/0TEST/result/')


