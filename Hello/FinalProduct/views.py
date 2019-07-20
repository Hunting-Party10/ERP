from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import Context
from django.template.loader import get_template
from .models import *
from . forms import *
from django.template.context_processors import csrf
from copy import deepcopy
from datetime import datetime


# Final Product----------------------------------------


def create_product(request):
    if request.POST:
        form = CreateProduct(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/fp/all')
    else:
        form = CreateProduct()
    args = {}
    args.update(csrf(request))
    args['form'] = form
    args.update({'final_products': Finalproduct.objects.all()})
    args.update({'progress_bar': 50})
    # create_product.html
    return render_to_response('table_create_product.html', args)


def final_product_list(request):
    Finalproduct_All_Obj = Finalproduct.objects.all()
    return render_to_response('tables.html', {'final_products': Finalproduct.objects.all()})


def final_product_components_by_id(request, final_product_id=1):
    components = Finalproduct.objects.get(
        id=final_product_id).component_list.all()
    print("jjjjjjjjjjjjjjjjjjjjjjj")
    progress = 0
    for comp in components:
        progress += comp.Progress

    # print(round((progress/components.count())))
    if components.count() != 0:
        progress = round((progress/components.count()))
        Finalproduct_Obj = Finalproduct.objects.get(
            id=final_product_id)
        Finalproduct_Obj.Progress = progress
        Finalproduct_Obj.save()

    return render_to_response('table_all_components.html', {'components': components, 'final_product_id': final_product_id, 'model': Finalproduct.objects.get(id=final_product_id)})


# For Componenets
def create_component(request, final_product_id=1):
    print("=============")
    form = CreateComponent(request.POST, request.FILES)
    if request.POST:
        try:
            # if the obj is alreday exit then add to that exiting obj
            Components_obj = Components.objects.get(
                Part_name=request.POST['Part_name'] and request.POST['Cheack_for_Allocation'] == False)
            print(Components_obj)
        except Components.DoesNotExist:
            Components_obj = -1

        if(Components_obj == -1):
            if form.is_valid():
                instance_of_component = form.save()
                new_instance_of_component = deepcopy(instance_of_component)
                print(
                    "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                print(new_instance_of_component)
                new_instance_of_component.Cheack_for_Allocation = True
                new_instance_of_component.id = None

                # new_instance_of_component.Rawmaterial_list.all().delete()
                new_instance_of_component.save()
                instance_of_component.delete()
                Finalproduct.objects.get(id=final_product_id).component_list.add(
                    new_instance_of_component)
                # Will add Recently add new components object from Components Class

                print(new_instance_of_component)
                return HttpResponseRedirect('/fp/get_components/' + str(final_product_id))
            else:
                form = CreateComponent()
        else:
            # Finalproduct.objects.add(Components.objects.get(Part_name = request.POST['Part_name']))
            new_instance_of_component = deepcopy(Components_obj)

            # print(new_instance_of_component)
            new_instance_of_component.Cheack_for_Allocation = True
            new_instance_of_component.Rawmaterial_list.all().delete()
            new_instance_of_component.save()
            Components_obj.delete()
            Finalproduct.objects.get(id=final_product_id).component_list.add(
                new_instance_of_component)

            # Finalproduct.objects.get(id=final_product_id).component_list.add(Components.objects.get(Part_name = request.POST['Part_name']))
            return HttpResponseRedirect('/fp/get_components/' + str(final_product_id))

    args = {}
    args.update(csrf(request))
    args.update({'form': form})
    args.update({'model': Finalproduct.objects.get(id=final_product_id)})
    args['components'] = Finalproduct.objects.get(
        id=final_product_id).component_list.all()
    return render_to_response('table_create_compoents.html', args)


def components_list_id(request, components_id=1):
    return render_to_response('get_by_id.html', {'component': Components.objects.get(id=component_id), 'component_id': components_id})


# Add process


def create_process(request, component_id=1):
    if request.POST:
        print("*********POST*****")
        print(request.POST)
        form = CreateProcess(request.POST, request.FILES)
        form_1 = CreateProcess()
        # Components.objects.get(id=component_id).process_list.add(
        # Process.objects.get(name=request.POST['Process_ID']))

        if form.is_valid():
            form.save()
            print("*********if*****")
            Components.objects.get(id=component_id).process_list.add(
                Process.objects.latest('pk'))
            # Will add Recently add new components object from Components Class
            return HttpResponseRedirect('/fp/get_component_info/' + str(component_id))
    else:
        print("*********else*****")
        form = CreateProcess()
    args = {}
    args.update(csrf(request))
    args.update({'form': form})
    args.update({'component': Components.objects.get(id=component_id)})
    args['process_list'] = Components.objects.get(
        id=component_id).Process_list
    args['All_Process_List'] = Process.objects.all()
    args['change_state'] = 0
    return render_to_response('Chainsetup.html', args)
    # return render_to_response('process_list_of_particular_component.html', args)


def change_process_status(request, component_id=1):
    # print(request.POST['value'])
    if request.POST:
        Day = 0  # For Date Purpose
        print(request.POST['name'])
    # print(request.POST.get("id"))
    # print(request.POST.get("value"))
        Comp_obj = Components.objects.get(id=component_id)
        print("++++++++++++++++++++++++++++++++++++++")
        if request.POST['name'] in Comp_obj.Process_list:
            # for v in Comp_obj.Process_list[request.POST['name']]
            if Comp_obj.Process_list[request.POST['name']][2] == "Completed":
                Comp_obj.Process_list[request.POST['name']][2] = "On Going"
            else:

                if Comp_obj.Process_list != "":
                    Total_process = len(Comp_obj.Process_list.items())
                    completed = 0
                    process = 0
                    for pro in Comp_obj.Process_list:
                        for status in Comp_obj.Process_list[pro]:
                            if status == "Completed":
                                completed += 1

                    Comp_obj.Progress = round((completed/Total_process)*100)
                    Comp_obj.save()
                else:
                    Comp_obj.Progress = 0
                    Comp_obj.save()

                d = Comp_obj.Process_list[request.POST['name']][1]
                date_format = "%Y-%m-%d"
                a = datetime.strptime('2019-07-20', date_format)
                b = datetime.strptime(d, date_format)
                delta = b - a
                Day = delta.days
                Comp_obj.Process_list[request.POST['name']][2] = "Completed"

        Comp_obj.save()
        print(request.POST)
        # pro = Components.objects.get(id=component_id).process_list.get(
        #     name=request.POST['name'])
        # pro.status = True
        # pro.save()
        args = {}
        args.update(csrf(request))
        name_Process = request.POST['name']
        # Comp_obj = Components.objects.get(id=component_id)
        print("/////////////////////////////////////")
        print(Comp_obj)
        # args.update({'form': form})
        args.update({'component': Components.objects.get(id=component_id)})
        args['process_list'] = Components.objects.get(
            id=component_id).process_list.all()
        args['All_Process_List'] = Process.objects.all()
        args['day'] = Day
        print("DayDayDayDayDayDayDayDayDayDayDayDayDayDayDay")
        print(Day)
        # Comp_obj.Process_list[request.POST['name']] = "OK"
        # Comp_obj.Process_list[name_Process] = [ "Compelted" , "Planned Date"  ,2 ]
        # Comp_obj.save()
        return render_to_response('Chainsetup.html', args)

        print("]]]]]]]]]]]]]]]]]]]]]]]")

        # return render_to_response('Chainsetup.html')
    return HttpResponseRedirect('/fp/change_process_status/' + component_id)


def Add_Process_to_Component(request, component_id=1):
    Comp_obj = Components.objects.get(id=component_id)  
    if Comp_obj.Process_list != "":
        Total_process = len(Comp_obj.Process_list.items())
        completed = 0
        process = 0
        for pro in Comp_obj.Process_list:
            for status in Comp_obj.Process_list[pro]:
                if status == "Completed":
                    completed += 1

        Comp_obj.Progress = round((completed/Total_process)*100)
        Comp_obj.save()
    else:
        Comp_obj.Progress = 0
        Comp_obj.save()
    if request.POST:
        print("*********POST*****")
        print(request.POST)
        form = CreateProcess(request.POST, request.FILES)
        form_1 = CreateProcess()
        Comp_obj = Components.objects.get(id=component_id)
        print(request.POST['Process_ID'])
        print("ppppppppppppppppppppppppppppp")

        if Comp_obj.Process_list == "":
            Comp_obj.Process_list = {request.POST['Process_ID']: [
                "Description", request.POST['Estimated-Date'], "On Going"]}
        else:
            Comp_obj.Process_list[request.POST['Process_ID']] = [
                "Description", request.POST['Estimated-Date'], "On Going"]
        Comp_obj.save()

        # Comp_obj.Process_list[request.POST['Process_ID']] = [
        #     "Description", "Planned Date", "On Going"]
        # Comp_obj.save()
        # Process.objects.get(name=request.POST['Process_ID']))

        if form.is_valid():
            form.save()
            print("*********if*****")
            # Components.objects.get(id=component_id).process_list.add(
            #     Process.objects.latest('pk'))
            # Will add Recently add new components object from Components Class
            return HttpResponseRedirect('/fp/get_component_info/' + component_id)
    else:
        print("*********else*****")
        form = CreateProcess()
    args = {}
    args.update(csrf(request))
    args.update({'form': form})
    args.update({'component': Components.objects.get(id=component_id)})
    args['process_list'] = Components.objects.get(
        id=component_id).process_list.all()
    args['All_Process_List'] = Process.objects.all()
    return render_to_response('Chainsetup.html', args)
    # return render_to_response('process_list_of_particular_component.html', args)


def get_components_details(request, component_id=1):
    Com_Obj = Components.objects.get(id=component_id)
    if Com_Obj.Process_list != "":
        Total_process = len(Com_Obj.Process_list.items())
        completed = 0
        process = 0
        for pro in Com_Obj.Process_list:
            for status in Com_Obj.Process_list[pro]:
                if status == "Completed":
                    completed += 1

        Com_Obj.Progress = round((completed/Total_process)*100)
        Com_Obj.save()

    else:
        Com_Obj.Progress = 0
        Com_Obj.save()

        # print(Comp_Obj.Process_list

    # for progress in Com_Obj.Process_list
    return render_to_response('table_Components_all_Details_RM.html', {'component': Components.objects.get(id=component_id),
                                                                       'progress': Com_Obj.Progress,
                                                                       'component_id': component_id, 'All_Process': Components.objects.get(id=component_id).process_list.all(),
                                                                       'Raw_Material': Components.objects.get(id=component_id).Rawmaterial_list})


def get_process_details_paticular_component(request, component_id=1):
    return render_to_response('process_list_of_particular_component.html', {'All_Process': Components.objects.get(id=component_id).process_list.all(),

                                                                            'component': Components.objects.get(id=component_id)})


# def Add_Process_to_Component():
#     pass


def Process_List(request):
    if request.method == 'POST':
        form = ProcessForm(request.POST)
        if form.is_valid():
            countries = form.cleaned_data.get('countries')
            # do something with your results
    else:
        form = CountryForm

    return render_to_response('render_country.html', {'form': form},
                              context_instance=RequestContext(request))


def Add_Process(request, component_id=1):
    if request.POST:
        Comp_obj = Components.objects.get(id=component_id)
        Process_name = request.POST["name"]
        Process_Date = int(request.POST["date"])
        Process_obj = Process.objects.get(name=Process_name)
        if Process_name in Comp_obj.Rawmaterial_list:
            Comp_obj.Rawmaterial_list[raw_material_name] += raw_material_quantity
        elif Comp_obj.Rawmaterial_list == "":
            Comp_obj.Rawmaterial_list = {
                Process_name: request.POST["status"]}
        else:
            print(Comp_obj.Rawmaterial_list)
            Comp_obj.Rawmaterial_list[raw_material_name] = raw_material_quantity
        Comp_obj.save()
        return HttpResponseRedirect("/fp/get_component_info/" + component_id)
    return HttpResponseRedirect("/fp/get_component_info/" + component_id)

# Delete Final Product


def delete_Final_Product(request, final_product_id=1):
    final_product_obj = get_object_or_404(Finalproduct, id=final_product_id)
    final_product_obj.delete()
    return HttpResponseRedirect('/fp/all')

#   Delete Delete Component


def delete_component(request, component_id=1, final_product_id=1):
    Components_obj = get_object_or_404(Components, id=component_id)
    final_product_obj = get_object_or_404(Finalproduct, id=final_product_id)
    final_product_obj.component_list.remove(Components_obj)
    return HttpResponseRedirect('/fp/all')

# ayushi


def ayushi(request):
    return render_to_response('Ayushi.html',  {'final_products': Finalproduct.objects.all()})

# def ayushi_search (request , )

# Assign Raw Material


def Create_Raw_Material(request):
    if request.POST:
        form = CreateRawMaterial(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/fp/all')
    else:
        form = CreateRawMaterial()
    args = {}
    args.update(csrf(request))
    args['form'] = form
    args.update({'Raw_Material': RawMaterial.objects.all()})
    args.update({'progress_bar': 50})
    # create_product.html
    return render_to_response('table_create_raw_material.html', args)


def Inventary(request):
    return render_to_response('table_raw_material_list.html', {'RawMaterial': RawMaterial.objects.all()})


def Assign_Raw_Material(request, component_id=1):
    return render(request, "Select_Quantity.html", {'Inventary': RawMaterial.objects.all(), 'component': Components.objects.get(id=component_id)})


def update_quantity_raw_material(request, component_id=1):
    if request.POST:
        Comp_obj = Components.objects.get(id=component_id)
        raw_material_name = request.POST["Inventary_ID"]
        raw_material_quantity = int(request.POST["quantity"])
        raw_material_obj = RawMaterial.objects.get(name=raw_material_name)
        raw_material_obj.quantity -= raw_material_quantity
        raw_material_obj.save()
        if raw_material_name in Comp_obj.Rawmaterial_list:
            Comp_obj.Rawmaterial_list[raw_material_name] += raw_material_quantity
        elif Comp_obj.Rawmaterial_list == "":
            Comp_obj.Rawmaterial_list = {
                raw_material_name: raw_material_quantity}
        else:
            print(Comp_obj.Rawmaterial_list)
            Comp_obj.Rawmaterial_list[raw_material_name] = raw_material_quantity
        Comp_obj.save()
        return HttpResponseRedirect("/fp/get_component_info/" + component_id)


'''
def index(request):
    name = "Prathamesh"
    html = "<html><body> Hi %s This seems to be Worked </body></html>" % name
    return HttpResponse(html)


def hello_templates(request):
    # print("In Final Product")
    name = "Prathamesh"
    # temp = get_template('hello.html')
    # html = temp.render(Context())
    # #return HttpResponse(html)
    return render_to_response('hello.html', {'name': name} )
'''
