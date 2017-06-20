from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views import View

from .models import Anime
from .forms import AnimeForm
from django.conf import settings

from operator import itemgetter

import os, time, datetime
from os import listdir
from os.path import isfile, isdir, join

import random
import string

MEDIA_ROOT = settings.MEDIA_ROOT

def index(request):
	return render(request, 'watchanime/home.html')
	
def about(request):
	return render(request, 'watchanime/basic.html', {'content':['This is simple website created by Ahmed Magdy to watch anime on local network','test']})

def generateCode(size=8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def episode_exists(folderName, episodeNumber):
	if(isdir(join(MEDIA_ROOT, folderName))):
		x = False
		for f in get_files(folderName):
			if f['episode'] == str(episodeNumber):
				x = True
			else:
				try:
					if int(f['episode']) == wanted_episode:
						return True
				except:
					return False
		return x

def SortAnimeFiles(animeList):
    swapped = True
    while(swapped):
        swapped = False
        for i in range(0, animeList.__len__() - 2):
            if(animeList[i]['episode'] > animeList[i + 1]['episode']):
                swapped = True
                temp = animeList[i]
                animeList[i] = animeList[i + 1]
                animeList[i + 1] = temp

    return animeList

def get_files(folder):
    path = MEDIA_ROOT+folder
    files = [f for f in listdir(path) if isfile(join(path, f))]
    newFilesList = []
    for f in files:
        date_modified = datetime.datetime.fromtimestamp(os.path.getmtime(join(path, f)))
        t = f.split()[-1].split('.')[0]
        g = 0
        try:
            g = int(t)
        except:
            g = t
        newFilesList.append({'path':f ,'episode': g, 'date_modified': date_modified, 'name': folder, 'hover': folder})
    try:	
        newFilesList = sorted(newFilesList, key=itemgetter('episode'))
    except:
	    pass
    return newFilesList

def reverse_list(files_list):
    new_list = []
    for f in files_list.__reversed__():
        new_list.append(f)
    return new_list

def get_all_folders_files(folder):
    path = MEDIA_ROOT + folder

    all_media_files = []
    dirs = [f for f in listdir(path) if isdir(join(path, f))]

    for dir in dirs:
        for file in get_files(dir):
            if file['name'].__len__() > 30:
                file['name'] = file['name'][:30] + '...'
            file['path'] = dir + '/' + file['path']
            all_media_files.append(file)

    return reverse_list(sorted(all_media_files, key=itemgetter('date_modified')))

def get_episode_path(animes_list, wanted_episode):
	for f in animes_list:
		if f['episode'] == str(wanted_episode):
			return f['path']
		else:
			try:
				if int(f['episode']) == wanted_episode:
					return f['path']
			except:
				return ""
	return ""

def handle_multiple_uploaded_files(folderName, startEpisode, files_uploded):
    fullFolderPath = join(MEDIA_ROOT, folderName)
    if not os.path.isdir(fullFolderPath):
        os.makedirs(fullFolderPath)
    for f in files_uploded:
        generatedFileName = generateCode() + ' ' + str(startEpisode)
        path = join(fullFolderPath, generatedFileName)
        with open(path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        startEpisode+=1

def handle_uploaded_file(folderName, fileName, fileData):
    if not os.path.isdir(MEDIA_ROOT + folderName):
        os.makedirs(MEDIA_ROOT + folderName)
    path = MEDIA_ROOT + folderName + fileName
    with open(path, 'wb+') as destination:
        for chunk in fileData.chunks():
            destination.write(chunk)

class upload_view(View):
    def post(self, request, *args, **kwargs):
        form = AnimeForm(request.POST, request.FILES)
        if(form.is_valid()):
            otherTitle = form.cleaned_data['otherTitle']
            folderName = form.cleaned_data['title'] + '\\'

            if otherTitle != None and otherTitle != "" and folderName == "Other group\\":
                folderName = otherTitle + '\\'
            
            if episode_exists(folderName, form.cleaned_data['episode']):
                context = {
                    'error': 'Episode exists already!, check the episode number'
                }
                return render(request, 'watchanime/upload_result.html', context)

            handle_multiple_uploaded_files(folderName, form.cleaned_data['episode'], request.FILES.getlist('file'))
            return render(request, 'watchanime/upload_result.html')
        if(form.errors):
            context = {
                'error': form.errors
            }
            return render(request, 'watchanime/upload_result.html', context)
        return HttpResponseRedirect('/')

    def get(self, request, *args, **kwargs):
        form = AnimeForm()
        context = {
            'title': "Upload your Anime!",
            'form': form
        }
        return render(request, 'watchanime/upload.html', context)

class HomeView(View):
    def get(self, request, *args, **kwargs):
        #try:
            dirs = [f for f in listdir(MEDIA_ROOT) if isdir(join(MEDIA_ROOT, f))]
            context = {
                'object_list': dirs,
                'recently_added': get_all_folders_files('')[:dirs.__len__()]
            }
            return render(request, 'watchanime/home.html', context)
        #except:
        #    return HttpResponse("<h1>HomeView error!</h1>")

class FolderView(View):
    def get(self, request, folderName=None):
        try:
            if(isdir(MEDIA_ROOT+folderName)):
                context = {
                    'title': folderName,
                    'files': get_files(folderName),
                    'recently_added': get_all_folders_files('')[:10]
                }
                return render(request, 'watchanime/folder.html', context)
            else:
                raise Http404()
        except:
            return HttpResponse("<h1>FolderView error!</h1>")

class VideoView(View):
    def get(self, request, folderName=None, fileName=None):
        #try:
            videoPath = folderName+'\\'+fileName
            files = get_files(folderName)
            episode = fileName.split()[-1].split('.')[0]
            try:
                episode = str(int(episode))
            except:
                episode = str(episode)
            if episode.isdigit() == False:
                nextEpisodePath = ''
                lastEpisodePath = ''
            else:
                nextEpisodePath = get_episode_path(files, int(episode)+1)
                lastEpisodePath = get_episode_path(files, int(episode)-1)

            if(os.path.exists(MEDIA_ROOT+videoPath)):
                context = {
                    'title': folderName,
                    'episode': episode,
                    'videoPath': videoPath,
                    'otherFiles': files,
                    'nextEpisode': nextEpisodePath,
                    'lastEpisode': lastEpisodePath
                }
                return render(request, 'watchanime/watch.html', context)
            else:
                raise Http404
        #except:
        #    return HttpResponse("<h1>VideoView error! Report to developer</h1>")