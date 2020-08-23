import ui
import sys
import dialogs
import requests
import webbrowser
import clipboard

from requests.auth import HTTPBasicAuth
from requests import Session

auth = HTTPBasicAuth(sys.argv[1], sys.argv[2])
rsession = Session()

@ui.in_background
def do_sort_playlist(sender):
	name = dialogs.input_alert(title="Playlist Name")
	
	if name and len(name) > 0:
		res = rsession.post("https://music.sarsoo.xyz/api/spotify/sort", 
		json={"playlist_name": name}, auth=auth)
		
		if 200 <= res.status_code < 300:
			output = 'Success'
		else:
			output = f'Failed {res.status_code} {res.body}'
		
		sender.superview['output_label'].text = output

@ui.in_background
def do_daily_scrobbles(sender):
	res = rsession.get("https://music.sarsoo.xyz/api/fm/today", auth=auth)

	if 200 <= res.status_code < 300:
		sender.superview['output_label'].text = str(res.json()['scrobbles_today'])
	else:
		sender.superview['output_label'].text = f'Failed {res.status_code} {res.body}'
	
@ui.in_background
def do_view_user(sender):
	res = rsession.get("https://music.sarsoo.xyz/api/user", auth=auth)

	if 200 <= res.status_code < 300:
		clipboard.set(res.text)
		webbrowser.open('jayson:///view?clipboard=true')
	else:
		sender.superview['output_label'].text = f'Failed {res.status_code} {res.body}'

@ui.in_background
def do_view_playlist(sender):
	name = dialogs.input_alert(title="Playlist Name")
	
	if name and len(name) > 0:
		res = rsession.get("https://music.sarsoo.xyz/api/playlist", params={'name': name}, auth=auth)
		
		if 200 <= res.status_code < 300:
			clipboard.set(res.text)
			webbrowser.open('jayson:///view?clipboard=true')
		else:
			sender.superview['output_label'].text = f'Failed {res.status_code} {res.body}'
			
@ui.in_background
def do_view_tag(sender):
	tag_id = dialogs.input_alert(title="Tag ID")
	
	if tag_id and len(tag_id) > 0:
		res = rsession.get(f"https://music.sarsoo.xyz/api/tag/{tag_id}", auth=auth)
		
		if 200 <= res.status_code < 300:
			clipboard.set(res.text)
			webbrowser.open('jayson:///view?clipboard=true')
		else:
			sender.superview['output_label'].text = f'Failed {res.status_code} {res.body}'
			
@ui.in_background
def do_run_playlist(sender):
	name = dialogs.input_alert(title="Playlist Name")
	
	if name and len(name) > 0:
		res = rsession.get("https://music.sarsoo.xyz/api/playlist/run", 
		params={"name": name}, auth=auth)
		
		if 200 <= res.status_code < 300:
			output = 'Success'
		else:
			output = f'Failed {res.status_code} {res.body}'
		
		sender.superview['output_label'].text = output

if __name__ == '__main__':
	v = ui.load_view()
	v.present('sheet')
