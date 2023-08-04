from django.contrib.auth.decorators import user_passes_test
# from django.shortcuts import redirect
# from functools import wraps


def verification_required(f):
    return user_passes_test(lambda u: u.is_verified, login_url='/verify')(f)


# def combined_required(view_func):
#     @wraps(view_func)
#     def _wrapped_view(request, *args, **kwargs):
#         # Check if the user is logged in
#         if not request.user.is_authenticated:
#             return redirect('home')  # Redirect to the home page

#         # Check if the user is verified
#         if not request.user.is_verified:
#             return redirect('home')  # Redirect to the home page

#         # If both checks pass, proceed with the original view function
#         return view_func(request, *args, **kwargs)

#     return _wrapped_view
