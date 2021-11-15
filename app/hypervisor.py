from app import app
from proxmoxer import ProxmoxAPI


hypervisor = app.config['HYPERVISOR']

proxmox = ProxmoxAPI(app.config['PROXMOX_HOST'], user=app.config['PROXMOX_USER'], token_name=app.config['PROXMOX_TOKEN_NAME'], token_value=app.config['PROXMOX_TOKEN_SECRET'], verify_ssl=False)

def get_virtual_machines():
    if hypervisor == 'proxmox':
        return proxmox.cluster.resources.get(type='vm')

def start_virtual_machine(vmid):
    if hypervisor == 'proxmox':
        return proxmox.nodes(app.config['PROXMOX_NODE']).qemu(vmid).status.start.post()

def shutdown_virtual_machine(vmid):
    if hypervisor == 'proxmox':
        return proxmox.nodes(app.config['PROXMOX_NODE']).qemu(vmid).status.shutdown.post()

def reset_virtual_machine(vmid):
    if hypervisor == 'proxmox':
        return proxmox.nodes(app.config['PROXMOX_NODE']).qemu(vmid).snapshot('default').rollback.post()