
category_list = {'General', 'Pets', 'Art'}

# [print(i) for i in category_list]

# category = {
#     "en": f"""
# Enter Category:

# <b>{[i for i in category_list]}</b>

# """,
#     "ru": f"""
# <b>{[i for i in category_list]}</b>

#         """
# }


category_list = ''.join([f'\n{i}' for i in category_list])
category_text = f"""
Select Product Category:
{category_list}
"""
