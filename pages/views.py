from django.views.generic import TemplateView
from products.models import Product, Category
from .forms import ContactForm
from django.shortcuts import render, redirect
from django.core.mail import send_mail

class HomePageView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        categories = Category.objects.all()
        
        products_by_category = []
        
        for category in categories:
            product = Product.objects.filter(category=category).order_by('-stock').first()
            if product:
                products_by_category.append(product)

        context['products'] = products_by_category
        return context
    
class AboutPageView(TemplateView):
    template_name = "pages/about.html"

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            email_message = f'name: {name}\nEmail: {email}\nMessage: {message}'

            send_mail(
                'Email from SolarBF from ' + name,
                email_message,
                email,
                ['johan.barragan@uabc.edu.mx']
            )
            return redirect('contact')
        else:
            print("Invalid Form")
    else:
        form = ContactForm()

    return render(request, 'pages/contact.html', {'form': form})