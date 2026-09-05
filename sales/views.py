import pandas as pd

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from .forms import CSVUploadForm
from .models import Sale


def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("dashboard")

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

    return render(request, "login.html")


def logout_view(request):

    logout(request)

    return redirect("login")


@login_required(login_url="/login/")
def upload_csv(request):

    if request.method == "POST":

        form = CSVUploadForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            csv_file = request.FILES["csv_file"]

            try:

                df = pd.read_csv(csv_file)

                required_columns = [
                    "order_id",
                    "order_date",
                    "customer_name",
                    "product_name",
                    "category",
                    "region",
                    "quantity",
                    "sales_amount",
                    "profit",
                ]

                if not all(
                    column in df.columns
                    for column in required_columns
                ):

                    messages.error(
                        request,
                        "Invalid CSV columns."
                    )

                    return redirect("upload_csv")

                for _, row in df.iterrows():

                    Sale.objects.update_or_create(

                        order_id=row["order_id"],

                        defaults={

                            "order_date": row["order_date"],
                            "customer_name": row["customer_name"],
                            "product_name": row["product_name"],
                            "category": row["category"],
                            "region": row["region"],
                            "quantity": row["quantity"],
                            "sales_amount": row["sales_amount"],
                            "profit": row["profit"],

                        }

                    )

                messages.success(
                    request,
                    "Sales CSV uploaded successfully!"
                )

                return redirect("upload_csv")

            except Exception as e:

                messages.error(
                    request,
                    f"Error: {e}"
                )

    else:

        form = CSVUploadForm()

    return render(
        request,
        "upload.html",
        {
            "form": form
        }
    )


@login_required(login_url="/login/")
def dashboard(request):

    sales_data = Sale.objects.all()

    city = request.GET.get("city")
    product = request.GET.get("product")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")


    if city:

        sales_data = sales_data.filter(
            region=city
        )


    if product:

        sales_data = sales_data.filter(
            product_name=product
        )


    if start_date:

        sales_data = sales_data.filter(
            order_date__gte=start_date
        )


    if end_date:

        sales_data = sales_data.filter(
            order_date__lte=end_date
        )


    total_sales = sales_data.aggregate(
        total=Sum("sales_amount")
    )["total"] or 0


    total_profit = sales_data.aggregate(
        total=Sum("profit")
    )["total"] or 0


    total_orders = sales_data.count()


    total_quantity = sales_data.aggregate(
        total=Sum("quantity")
    )["total"] or 0


    city_sales = (

        sales_data

        .values("region")

        .annotate(
            total=Sum("sales_amount")
        )

        .order_by("-total")

    )


    # PRODUCT SALES + UNIT PRICE

    product_sales = (

        sales_data

        .values("product_name")

        .annotate(
            total=Sum("sales_amount"),
            total_quantity=Sum("quantity")
        )

        .order_by("-total")[:5]

    )


    for product in product_sales:

        if product["total_quantity"]:

            product["unit_price"] = (
                product["total"] /
                product["total_quantity"]
            )

        else:

            product["unit_price"] = 0


    customer_sales = (

        sales_data

        .values("customer_name")

        .annotate(
            total=Sum("sales_amount")
        )

        .order_by("-total")[:5]

    )


    monthly_sales = (

        sales_data

        .values("order_date__month")

        .annotate(
            total=Sum("sales_amount")
        )

        .order_by("order_date__month")

    )


    cities = (

        Sale.objects

        .values_list(
            "region",
            flat=True
        )

        .distinct()

        .order_by("region")

    )


    products = (

        Sale.objects

        .values_list(
            "product_name",
            flat=True
        )

        .distinct()

        .order_by("product_name")

    )


    context = {

        "total_sales": total_sales,

        "total_profit": total_profit,

        "total_orders": total_orders,

        "total_quantity": total_quantity,

        "city_sales": city_sales,

        "product_sales": product_sales,

        "customer_sales": customer_sales,

        "monthly_sales": monthly_sales,

        "cities": cities,

        "products": products,

        "selected_city": city,

        "selected_product": product,

        "start_date": start_date,

        "end_date": end_date,

    }


    return render(
        request,
        "dashboard.html",
        context
    )