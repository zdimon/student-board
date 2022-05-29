
def roles_processor(request):
    role = 'undefine'
    try:
        prof = request.user.student
        role = 'student'
    except:
        pass

    try:
        prof = request.user.mentor
        role = 'mentor'
    except:
        pass
             
    return {'role': role}