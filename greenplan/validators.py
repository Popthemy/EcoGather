# from django.core.exceptions import ValidationError

# def datetime_validator(event,value):
#   start = event.start_datetime
#   end = event.end_datetime
#   if value == start  and start <= end:
#     raise ValidationError({'Start_datetime':f' The start:{str(start)} must be less than or equal to the  end: {str(end)} '})
  
#   if value == end  and end >= start:
#     raise ValidationError({'End_datetime': f'The end: {str(end)} must be greater than or equal to the {start}'})
    
    