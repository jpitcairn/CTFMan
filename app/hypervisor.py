from app import app
from proxmoxer import ProxmoxAPI


hypervisor = app.config['HYPERVISOR']

proxmox = ProxmoxAPI(app.config['PROXMOX_HOST'], user=app.config['PROXMOX_USER'], token_name=app.config['PROXMOX_TOKEN_NAME'], token_value=app.config['PROXMOX_TOKEN_SECRET'], verify_ssl=False)

def get_hypervisor_nodes():
    nodes = []
    if hypervisor == 'proxmox':
        for node in proxmox.nodes.get():
            nodes.append(node['node'])
        return nodes

def get_virtual_machines():
    if hypervisor == 'proxmox':
        return proxmox.cluster.resources.get(type='vm')

def get_node_virtual_machines(node=get_hypervisor_nodes()[0]):
    vmsArray = []
    if hypervisor == 'proxmox':
        for vm in proxmox.nodes(node).qemu.get():
            vmsObj = {}
            vmsObj['id'] = vm['vmid']
            vmsObj['name'] = vm['name']
            vmsArray.append(vmsObj)
        return vmsArray

def start_virtual_machine(vmid):
    if hypervisor == 'proxmox':
        return proxmox.nodes(app.config['PROXMOX_NODE']).qemu(vmid).status.start.post()

def shutdown_virtual_machine(vmid):
    if hypervisor == 'proxmox':
        return proxmox.nodes(app.config['PROXMOX_NODE']).qemu(vmid).status.shutdown.post()

def reset_virtual_machine(vmid):
    if hypervisor == 'proxmox':
        return proxmox.nodes(app.config['PROXMOX_NODE']).qemu(vmid).snapshot('default').rollback.post()