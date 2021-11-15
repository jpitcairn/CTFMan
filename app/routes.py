from flask import render_template, flash, redirect, url_for
from app import app, forms
from app.hypervisor import get_virtual_machines, start_virtual_machine, shutdown_virtual_machine, reset_virtual_machine
from app.forms import EmptyForm

@app.route('/')
@app.route('/home')
def home():
    user = {'username':'Jordan'}
    form = EmptyForm()
    virtual_machines = get_virtual_machines()
    return render_template('index.html', title='Home', slug='Control VMs', virtual_machines=virtual_machines, form=form, user=user)

# Start Virtual Machine
@app.route('/vm/start/<vmid>', methods=['POST'])
def start_vm(vmid):
    form = EmptyForm()
    if form.validate_on_submit():
        start_virtual_machine(vmid)
        flash('Starting Virtual Machine.')
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

# Shutdown Virtual Machine
@app.route('/vm/shutdown/<vmid>', methods=['POST'])
def shutdown_vm(vmid):
    form = EmptyForm()
    if form.validate_on_submit():
        shutdown_virtual_machine(vmid)
        flash('Shutting down Virtual Machine.')
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

# Reset Virtual Machine
@app.route('/vm/reset/<vmid>', methods=['POST'])
def reset_vm(vmid):
    form = EmptyForm()
    if form.validate_on_submit():
        reset_virtual_machine(vmid)
        flash('Resetting Virtual Machine.')
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))