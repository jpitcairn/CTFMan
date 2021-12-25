from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, forms, db
from app.hypervisor import get_node_virtual_machines, get_virtual_machines, start_virtual_machine, shutdown_virtual_machine, reset_virtual_machine
from app.forms import AddVMForm, EditVMForm, EmptyForm, LoginForm, RegisterForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, VirtualMachine
from werkzeug.urls import url_parse

# Index page routing
@app.route('/')
@app.route('/home')
@login_required
def home():
    form = EmptyForm()
    virtual_machines = VirtualMachine.query.order_by(VirtualMachine.id.desc())
    return render_template('index.html', title='Home', slug='Control VMs', virtual_machines=virtual_machines, form=form)

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)

# Logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# Register

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect (url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registered Successfully')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

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


# Admin Section

# Users View
@app.route('/admin/users')
@login_required
def admin_users():
    users = User.query.order_by(User.id.desc())
    return render_template('admin/users.html', title='Home', slug='Control VMs', users=users)

# VM's View
@app.route('/admin/vm', methods=['GET', 'POST'])
@login_required
def admin_vms():
    form = AddVMForm()
    virtual_machines = VirtualMachine.query.order_by(VirtualMachine.id.desc())
    form.vm_id.choices = [(vm['id'], vm['name'] + " (" + str(vm['id']) + ")" ) for vm in get_node_virtual_machines()]
    
    if request.method == 'POST':
        if form.validate_on_submit():
            vm = VirtualMachine(vm_id=form.vm_id.data, node=form.node.data)
            db.session.add(vm)
            db.session.commit()
        flash('VM Added Successfully')
    
    return render_template('admin/vms.html', title="Virtual Machines", slug="Manage CTF VM's", form=form, virtual_machines=virtual_machines)

@app.route('/admin/vm/<id>/edit', methods=['GET', 'POST'])
def admin_edit_vm(id):
    form = EditVMForm()
    vm = VirtualMachine.query.filter_by(id=id).first_or_404()
    form.validate_on_submit():
    



    render_template('admin/edit_vm.html', vm)

# API Routes 

@app.route('/vms/<node>')
@login_required
def node_vms(node):
    vms = get_node_virtual_machines(node)
    return jsonify({'vms' : vms})
