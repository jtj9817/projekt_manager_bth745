from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request, 'index.html')

def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return render(request, 'index.html')
			else:
				return render(request, 'login.html', {'error_message': 'Account is disabled.'})
		else:
			return render(request, 'login.html', {'error_message': 'Invalid login'})
	return render(request, 'login.html')	

#User submits the form filled with data in a POST request
def register(request):
	if request.method == 'POST':
		form = UserForm(request.POST)
		if form.is_valid():
			user= form.save(commit=False)
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user.set_password(password)
			user.save()
			user = authenticate(username=username, password=password)
			login(request, user)
			return render(request,'registersuccess.html')
	else:
		form = UserForm()
	return render(request, 'registration_form.html', {'form': form})
