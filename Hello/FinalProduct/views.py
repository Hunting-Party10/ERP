from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import Context
from django.template.loader import get_template
from .models import *
from . forms import *
from django.template.context_processors import csrf
from copy import deepcopy
from datetime import datetime as dt
import datetime
from django.forms import model_to_dict










# Final Product----------------------------------------

def Final_Product_List_Item_Master(request):
    return render_to_response('Final_Product_List.html' , { 'final_products' : Finalproduct.objects.all()})
    
def Item_Master(request):
    return render_to_response('Item_Master_On_Click_Page.html')

def Components_List_Item_Master(request):
    return render_to_response('Components_List.html' , { 'components_list' : Components.objects.all()})

def Inventory_List_Item_Master(request):
    return render_to_response('Inventory_List_Item_Master.html' , { 'Inventory_List' : RawMaterial.objects.all()})

def create_product(request):
    if request.POST:
        form = CreateProduct(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/fp/Final_Product_List')
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
    # Finalproduct_All_Obj = Finalproduct.objects.all()
    # components = Finalproduct.objects.get(
        # id=final_product_id).component_list.all()
    print("jjjjjjjjjjjjjjjjjjjjjjj")
    progress = 0
    Finalproduct_All_Obj = Finalproduct.objects.all()

    for i in range(Finalproduct.objects.all().count()):
        progress = 0
        # progress += Finalproduct_All_Obj[i].Progress
        fp = Finalproduct_All_Obj[i]
        # print(Finalproduct_All_Obj[i])
        for i in fp.component_list.all():
            progress += i.Progress
        if fp.component_list.all().count() != 0:
            fp.Progress = progress/fp.component_list.all().count()
            fp.save()
            # print(fp.name)
            # print(fp.Progress)
        else:
            fp.Progress = 0
            fp.save()
        # Finalproduct.objects.get(name=i.name).Progress = progress

    # print(progress)
    # for counter in range(Finalproduct.objects.all().count()):
    #     components = Finalproduct.objects.get(id=116).component_list.all()
    #     for comp in components:
    #         progress += comp.Progress

    # # print(round((progress/components.count())))
    # if components.count() != 0:
    #     progress = round((progress/components.count()))
    #     Finalproduct_Obj = Finalproduct.objects.get(
    #         id=final_product_id)
    #     Finalproduct_Obj.Progress = progress
    #     Finalproduct_Obj.save()

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

def Create_Component(request):
  
    if request.POST:
        form = CreateComponent(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/fp/Components_List/')
    else:
        form = CreateComponent()
    args = {}
    args.update(csrf(request))
    args['form'] = form
    args.update({ 'components_list' : Components.objects.all()})
                
    return render_to_response('Create_Component_To_DataBase.html' , args)    



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
    Comp_obj = Components.objects.get(id=component_id)
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
        print("*********else*************")
        form = CreateProcess()
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
    args = {}
    args.update(csrf(request))
    args.update({'form': form})
    args.update({'component': Components.objects.get(id=component_id)})
    args['process_list'] = Components.objects.get(
        id=component_id).Process_list
    args['All_Process_List'] = Process.objects.all()
    args['change_state'] = 0
    return render_to_response('Process_List.html', args)
    # return render_to_response('process_list_of_particular_component.html', args)


def change_process_status(request, component_id=1):
    if request.POST:
        print("Date***************Date******************Date")
        # print(datetime.today().strftime('%Y-%m-%d'))
        Day = 0  # For Date Purpose
        Comp_obj = Components.objects.get(id=component_id)
        # print("++++++++++++++++++++++++++++++++++++++")
        if request.POST['name'] in Comp_obj.Process_list:
            print("++++++++++++++++++++++++++++++++++++++")
            if Comp_obj.Process_list[request.POST['name']][2] == "None":
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
                
                # date_format = "%Y-%m-%d"
                # Expected_Date = Comp_obj.Process_list[request.POST['name']][1] # Expected Date
                # # Expected_Date_Obj = datetime.datetime.strftime(Expected_Date,'%Y-%m-%d')

                # # print(Expected_Date.strftime("%d/%m/%Y"))
                # Expected_Date = dt.strptime(Expected_Date, '%Y-%m-%d')
                # print(Expected_Date)
                # # date_format = "%Y-%m-%d"
                # Today_Date = dt.today()
                # print(Today_Date)
                #a = datetime.strptime('2019-07-20', date_format)
                # Today_Date= Today_Date.strftime( "%Y-%m-%d")
                # a = (datetime.datetime.strftime(Today_Date, date_format).strftime('%Y-%m-%d'))        # Today's Date
                # b = (datetime.datetime.strftime(str(Expected_Date).split(' ')[0], date_format).strftime('%Y-%m-%d'))
                # # print(datetime.strptime(Expected_Date, date_format))
                # delta = b - a
                # Day = delta.days
                print("Day------------------")
                
                Expected_Date = Comp_obj.Process_list[request.POST['name']][1] # Expected Date
                Today_Date =dt.today().strftime('%Y-%m-%d')
                
                date_format = "%Y-%m-%d"
                
                
                print("Expected_Date ==> " + str(Expected_Date) )
                Today_Date = datetime.datetime.strptime(Today_Date, date_format)
                print("Today_Date ==> " + str(Today_Date) )
                
                Expected_Date = datetime.datetime.strptime(Expected_Date, date_format)
                print("Expected_Date ==> " + str(Expected_Date) )
                print(type(Today_Date))
                print(Today_Date)
                # Day = Today_Date - Expected_Date
                # print(Day.date)
                print(type(Expected_Date))
                
                Day = Expected_Date - Today_Date
                Completion_Time = Day.days
                Comp_obj.Process_list[request.POST['name']][4] = "Completed"
                Comp_obj.Process_list[request.POST['name']][2] = dt.today().strftime('%Y-%m-%d')
                if Completion_Time > 0:
                    Comp_obj.Process_list[request.POST['name']][3] = ("Done Before " + str(Completion_Time) + " Days")
                else:
                    Comp_obj.Process_list[request.POST['name']][3] = ( "Delayed by " + str(abs(Completion_Time)) + " Days" )
            else:
                Comp_obj.Process_list[request.POST['name']][2] = "None"
                Comp_obj.Process_list[request.POST['name']][3] = "None"
                Comp_obj.Process_list[request.POST['name']][4] = "On Going"
        Comp_obj.save()
        args = {}
        args.update(csrf(request))
        name_Process = request.POST['name']
        print("/////////////////////////////////////")
        args.update({'component': Components.objects.get(id=component_id)})
        args['process_list'] = Components.objects.get(
            id=component_id).process_list.all()
        args['All_Process_List'] = Process.objects.all()
        
        
        print("]]]]]]]]]]]]]]]]]]]]]]]")
        # return render_to_response('Process_List.html', args)
        return HttpResponseRedirect('/fp/get_porcess_info/' + str(component_id))
    return HttpResponseRedirect('/fp/get_porcess_info/' + str(component_id))


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
        print(request.POST)
        print("ppppppppppppppppppppppppppppp")

        if Comp_obj.Process_list == "":
            Comp_obj.Process_list = {request.POST['Process_ID']: [
                request.POST['Description'], request.POST['Estimated-Date'],"None" ,"None", "On Going"]}
        else:
            Comp_obj.Process_list[request.POST['Process_ID']] = [
                request.POST['Description'], request.POST['Estimated-Date'],"None" ,"None", "On Going"]
        Comp_obj.save()

        # if form.is_valid():
        #     form.save()
        #     print("*********if*****")
        return HttpResponseRedirect('/fp/get_porcess_info/' + component_id)
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
    return render_to_response('Process_List.html', args)
    # return render_to_response('Chainsetup.html', args)
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
    return HttpResponseRedirect('/fp/Final_Product_List')

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
    return render(request, "select_quantity_template.html", {'Inventary': RawMaterial.objects.all(), 'component': Components.objects.get(id=component_id)})


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


#-----------------------------New Ordert---------------------------------------------------------------


def PO_Status(request , customer_id=1):
    Customer_Obj = Customer.objects.get(id=customer_id)
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print(Purchase_Order.objects.filter(customer_id__in=Customer.objects.filter(id=customer_id))) #get all object Reference by foregin key
    return render_to_response('PO_List_Of_Customer.html' , {'PO_List' : Purchase_Order.objects.filter(customer_id__in=Customer.objects.filter(id=customer_id)) , 'customer_id' : customer_id ,'Customer_Obj':Customer_Obj })


def create_purchase_order(request,customer_id=1):
    if request.POST:
        form = CreatePO(request.POST)
        if form.is_valid():
            print("$$$$$$$$$$$$$$$$$$$$")
            # print(form['id'].value())
            form.instance.customer = Customer.objects.get(id=customer_id)
            #Add Purchase Corresponding to Specific Customer(Foregin Key)
            print(form.instance.customer)
            form.save()
            return HttpResponseRedirect('/fp/PO_Status/' + customer_id)
    else:
        form = CreatePO()
    args = {}
    args.update(csrf(request))
    args['form'] = form
    args['Customer_Obj'] = Customer.objects.get(id=customer_id)
    args.update({'PO_List': Purchase_Order.objects.filter(customer_id__in=Customer.objects.filter(id=customer_id))})
    # create_product.html
    return render_to_response('table_create_purchase_order.html', args)





def create_customer(request):
    if request.POST:
        form = CreateCustomer(request.POST)
        if form.is_valid():
            form.save() 
            return HttpResponseRedirect('/fp/customer_list')
    else:
        form = CreateCustomer()
    args = {}
    args.update(csrf(request))
    args['form'] = form
    args.update({'Customer_List': Customer.objects.all()})
    # create_product.html
    return render_to_response('table_create_customer.html', args)


def customer_list(request):
    print(Customer.objects.all())
    return render_to_response('Customer_List.html', {'Customer_List': Customer.objects.all()})


def Select_Assembly_to_Po(request,po_id=1):
    Purchase_Order_objects = (Purchase_Order.objects.get(id=po_id))
    print(":::::::::::::::::::::::::::::::::::::")
    args = {}
    args['Purchase_Order_objects'] = Purchase_Order_objects
    args['All_Final_Product_List'] = Finalproduct.objects.all()
    args.update(csrf(request))
    print(Finalproduct.objects.all())
    return render_to_response('Select_Final_Product_For_PO.html', args)


def show_selected_final_product_components_list(request , po_id=1):
    if request.POST:
        print("============")
        Original_Obj = Finalproduct.objects.get(id=request.POST['Select_All'])
        kwargs = model_to_dict(Original_Obj , exclude=['id','component_list'])
        new_obj_for_particular_po = Finalproduct.objects.create(**kwargs)
        new_obj_for_particular_po.In_DataBase = False
        new_obj_for_particular_po.Progress = 0
        for i in Original_Obj.component_list.all():
            new_component = deepcopy(i)
            new_component.Progress = 0
            new_component.id = None
            new_component.save()
            new_obj_for_particular_po.component_list.add(new_component)
            new_obj_for_particular_po.save()
        Purchase_Order_objects = Purchase_Order.objects.get(id=po_id)
        Purchase_Order_objects.Final_Product_list.add(new_obj_for_particular_po)
        Purchase_Order_objects.save()
        args = {}
        args['All_Final_Product_List'] = Finalproduct.objects.all()
        args.update(csrf(request))
        args['Purchase_Order_objects'] = Purchase_Order_objects
        # args['Purchase_Order_Obj'] = Purchase_Order_Obj;
        print("=============================")
    else:
        args['All_Final_Product_List'] = Finalproduct.objects.all()
        # args.update(csrf(request))
        args['Purchase_Order_objects'] = Purchase_Order_objects
    return render_to_response('Select_Final_Product_For_PO.html', args)
    

def Select_Components_For_PO(request , po_id=1 , final_product_id=1):
    if request.POST:
        print("")
        print("OK")
        print("`````````````````````````````")
        Selected_Components = request.POST.getlist('checks')
        Original_Obj = Finalproduct.objects.get(id=final_product_id)
        kwargs = model_to_dict(Original_Obj , exclude=['id','component_list'])
        new_obj_for_particular_po = Finalproduct.objects.create(**kwargs)
        new_obj_for_particular_po.In_DataBase = False
        new_obj_for_particular_po.Progress = 0
        for i in Selected_Components:
            New_Components = deepcopy(Components.objects.get(id=i))
            New_Components.Progress = 0
            New_Components.id = None
            New_Components.save()
            new_obj_for_particular_po.component_list.add(New_Components)
            new_obj_for_particular_po.save()
        
        args = {}
        args['All_Final_Product_List'] = Finalproduct.objects.all()
        args.update(csrf(request))
        Purchase_Obj = Purchase_Order.objects.get(id=po_id)
        Purchase_Obj.Final_Product_list.add(new_obj_for_particular_po)
        Purchase_Obj.save()
        args['Purchase_Order_objects'] = Purchase_Obj
        

        return render_to_response('Select_Final_Product_For_PO.html', args)

        
        
    
    args = {}
    args.update(csrf(request))
    args['Finalproduct_components_list'] = Finalproduct.objects.get(id=final_product_id).component_list.all
    args['Final_Product_id'] = final_product_id
    args['Purchase_Order_objects_id'] = po_id
    return render_to_response('Select_Components_For_PO.html', args)



def Assembly_Status(request):
    args = {}
    PO_Progress = 0
    Total_Assembly = 0
    args['PO'] = Purchase_Order.objects.all()
    print("?/////////////////")
    for i in Purchase_Order.objects.all():
        for j in i.Final_Product_list.all():
            PO_Progress = PO_Progress + (j.Progress)
            Total_Assembly = Total_Assembly + 1 
        if(Total_Assembly != 0):
            i.Progress = round((PO_Progress / Total_Assembly))
        else:
            i.Progress = 0
        Total_Assembly = 0
        PO_Progress = 0
        
            
        
    return render_to_response('Assembly_Status.html' , args)



def Approved_PO_List(request):
    args = {}
    args['PO_List'] = Purchase_Order.objects.all()
    return render_to_response('Approved_PO_List.html' , args)
     



def get_component_info_of_selected_assembly(request, final_product_id=1):
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

    return render_to_response('List_Of_Selected_Components.html', {'components': components, 'final_product_id': final_product_id, 'model': Finalproduct.objects.get(id=final_product_id)})

'''def index(request):
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
