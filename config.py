import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))



class Config(object):
    # Choice of hypervisor proxmox, esxi, azure
    HYPERVISOR = os.environ.get('HYPERVISOR')
    # proxmox host settings
    PROXMOX_HOST = os.environ.get('PROXMOX_HOST')
    PROXMOX_USER = os.environ.get('PROXMOX_USER')
    PROXMOX_TOKEN_NAME = os.environ.get('PROXMOX_TOKEN_NAME')
    PROXMOX_TOKEN_SECRET = os.environ.get('PROXMOX_TOKEN_SECRET')
    # CSRF token
    SECRET_KEY = os.environ.get('SECRET_KEY')
