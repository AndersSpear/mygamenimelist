from flask import Blueprint, redirect, url_for, render_template, flash, request, session
from flask_login import current_user, login_required, login_user, logout_user
from flask_dance.contrib.discord import make_discord_blueprint, discord
import xmltodict
from urllib import parse
from .. import bcrypt
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm
from ..models import User, load_user
import requests
import os
import json

#heres a commnet
API_ENDPOINT = 'https://discord.com/api/v10'
REDIRECT_URI = 'https://msl.aspear.cs.umd.edu/callback'

discordd = make_discord_blueprint(
    client_id=os.environ["DISCORD_CLIENT_ID"],
    client_secret=os.environ["DISCORD_CLIENT_SECRET"],
    redirect_url=REDIRECT_URI,
)


@discordd.route("/cascallback")
def cascallback():
    ticket = request.args['ticket']
    resp = requests.get("https://shib.idm.umd.edu/shibboleth-idp/profile/cas/serviceValidate", params={"service":"https://msl.aspear.cs.umd.edu/","ticket":ticket})
    r = xmltodict.parse(resp.content)
    print(resp.url)
    print(r)
    if 'cas:authenticationSuccess' in r:
        username = r['user']
        discord_user_id = user_info['user']['id']

        # resp3 = requests.get('https://discord.com/api/users/@me', headers={
        #     'Authorization': f'Bearer {access_token}'
        # })
        # user_data = resp3.jsonn()
        # #email = user_data['email']
        #user = User.objects(discord_user_id=discord_user_id).first()
        #if user is None:
        #    user = User(username=username, discord_user_id=discord_user_id)
        #    user.save()

        #ogin_user(user)
        return redirect(url_for("users.account"))
    else:
        return render_template("404.html")
# @discordd.route("/")
# def index():
#     if not discord.authorized:
#         return redirect(url_for("discord.login"))
#     resp = discord.get("/api/users/@me")
#     return redirect(url_for('discord.logout'))


@discordd.route("/callback")
def callback():

    code = request.args['code']
    data = {
        'client_id': os.environ["DISCORD_CLIENT_ID"],
        'client_secret': os.environ["DISCORD_CLIENT_SECRET"],
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    resp = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers)
    jsonn = resp.json()
    #print(type(jsonn))
    #print(json.dumps(jsonn))
    access_token = jsonn['access_token']

    new_headers = {"Authorization": f"Bearer {access_token}"}
    resp2 = requests.get("https://discord.com/api/oauth2/@me", headers=new_headers)
    if resp2.status_code == 200:
        user_info = resp2.json()
        username = user_info['user']['username']
        discord_user_id = user_info['user']['id']

        # resp3 = requests.get('https://discord.com/api/users/@me', headers={
        #     'Authorization': f'Bearer {access_token}'
        # })
        # user_data = resp3.jsonn()
        # #email = user_data['email']
        user = User.objects(discord_user_id=discord_user_id).first()
        if user is None:
            user = User(username=username, discord_user_id=discord_user_id)
            user.save()

        login_user(user)
        return redirect(url_for("users.account"))
    else:
        return render_template("404.html")


@discordd.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))
