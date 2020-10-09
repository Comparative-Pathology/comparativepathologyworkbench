from django.contrib.auth.models import User

from rest_framework import serializers

from matrices.models import Matrix
from matrices.models import Cell
from matrices.models import Image
from matrices.models import Server
from matrices.models import Type

from django.db import models
from django.db.models import Q 


"""

    This Serializer provides Create, Read, Update and Delete functions for an Image

"""
class ImageSerializer(serializers.HyperlinkedModelSerializer):

    roi = serializers.IntegerField(default=0)
    owner = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    server = serializers.CharField()
    image_id = serializers.IntegerField(default=0)
    
    class Meta:
        model = Image
        fields = ('url', 'id', 'owner', 'roi', 'server', 'image_id')
        read_only_fields = ('id', 'url' )
        

    """
        Image Serializer, Create Method
    """
    def create(self, validated_data):
    
        #print("Image Serializer, Create")

        image_active = True
        image_server = validated_data.get('server')
        image_owner = validated_data.get('owner')
        image_id = validated_data.get('image_id')
        image_roi_id = validated_data.get('roi')
        
        server = self.validate_image_json(image_server, image_owner, image_id, image_roi_id)
        
        image_identifier = int(image_id)

        image_name = ''
        image_viewer_url = ''
        image_birdseye_url = ''
        image_roi = 0
        
        if server.is_wordpress() == True:
        
            data = server.check_wordpress_image(image_owner, image_id)
        
            json_image = data['image']
            
            image_name = json_image['name']
            image_viewer_url = json_image['viewer_url']
            image_birdseye_url = json_image['birdseye_url']
	        
        else:
        
            data = server.check_imaging_server_image(image_owner, image_id)
        
            json_image = data['image']
            
            image_name = json_image['name']
            image_viewer_url = json_image['viewer_url']
            image_birdseye_url = json_image['birdseye_url']
            
            if image_roi_id != 0:
                
                data = server.check_imaging_server_image_roi(image_owner, image_id, image_roi_id)

                json_roi = data['roi']
                
                image_roi = int(json_roi['id'])
                        
        image = Image.create(image_id, image_name, server, image_viewer_url, image_birdseye_url, image_active, image_roi, image_owner)

        image.save()

        return image


    """
    Image Serializer, Update Method
    """
    def update(self, instance, validated_data):
    
        #print("Image Serializer, Update")

        image_active = True
        image_server = validated_data.get('server')
        image_owner = validated_data.get('owner', instance.owner)
        image_id = validated_data.get('image_id', instance.image_id)
        image_roi_id = validated_data.get('roi', instance.roi)

        server = self.validate_image_json(image_server, image_owner, image_id, image_roi_id)
        
        image_identifier = int(image_id)
        image_name = ''
        image_viewer_url = ''
        image_birdseye_url = ''
        image_roi = 0
        
        if server.is_wordpress() == True:
        
            data = server.check_wordpress_image(image_owner.id, image_id)
        
            json_image = data['image']
            
            image_name = json_image['name']
            image_viewer_url = json_image['viewer_url']
            image_birdseye_url = json_image['birdseye_url']
	        
        else:
        
            data = server.check_imaging_server_image(image_owner.id, image_id)
        
            json_image = data['image']
            
            image_name = json_image['name']
            image_viewer_url = json_image['viewer_url']
            image_birdseye_url = json_image['birdseye_url']
            
            if image_roi_id != 0:
                
                data = server.check_imaging_server_image_roi(image_owner, image_id, image_roi_id)

                json_roi = data['roi']
                
                image_roi = int(json_roi['id'])
                        
        instance.server = server
        instance.owner = image_owner
        instance.image_id = image_id
        instance.identifier = image_id
        instance.name = image_name
        instance.viewer_url = image_viewer_url
        instance.birdseye_url = image_birdseye_url
        instance.roi = image_roi

        instance.save()

        return instance


    """
        Image Serializer, For an Image, Validate the supplied Server, Owner, Image Id and ROI ID Fields
    """
    def validate_image_json(self, server_str, user, image_id, roi_id):
    
        server_list = server_str.split("@")
        
        server_uid = str(server_list[0])
        server_url = str(server_list[1])
        
        if Server.objects.filter(Q(uid=server_uid) & Q(url_server=server_url)).exists():

            server = Server.objects.get(Q(uid=server_uid) & Q(url_server=server_url))
        
            if server.is_wordpress() == True:
                
                if self.validate_wordpress_image_id(server, user, image_id) == False:

                    message = 'ERROR! Image NOT Present on : ' + server_str
                    raise serializers.ValidationError(message)
            else:

                if server.is_omero547() == True or server.is_omero56() == True:

                    if self.validate_imaging_image_id(server, user, image_id) == True:
                
                        if roi_id != 0:
                    
                            if self.validate_roi_id(server, user, image_id, roi_id) == False:
                            
                                message = 'ERROR! ROI ID ' + str(roi_id) + ', for Image ID ' + str(image_id) + ", NOT Present on : " + server_str
                                raise serializers.ValidationError(message)
                    else:

                        message = 'ERROR! Image ID ' + str(image_id) + ', NOT Present on : ' + server_str
                        raise serializers.ValidationError(message)
                else:

                    message = 'ERROR! Server Type Unknown : ' + server_str
                    raise serializers.ValidationError(message)

            return server

        else:

            message = 'ERROR! Server Unknown : ' + server_str
            raise serializers.ValidationError(message)

            return None


    """
        Image Serializer, For a Wordpress Image, Check the supplied Image Exists
    """
    def validate_wordpress_image_id(self, server, user, image_id):
    
        data = server.check_wordpress_image(user, image_id)
        
        image_name = data['name']

        if image_name == "":
            return False
        else:
            return True


    """
        Image Serializer, For an OMERO Image, Check the supplied Image Exists
    """
    def validate_imaging_image_id(self, server, user, image_id):
    
        data = server.check_imaging_server_image(user, image_id)
        
        json_image = data['image']
        image_name = json_image['name']
        
        if image_name == "":
            return False
        else:
            return True


    """
        Image Serializer, For an OMERO Image ROI, Check the supplied ROI Exists
    """
    def validate_roi_id(self, server, user, image_id, roi_id):
    
        data = server.check_imaging_server_image_roi(user, image_id, roi_id)

        json_roi = data['roi']
        roi_id = json_roi['id']

        if roi_id == "":
            return False
        else:
            return True


"""

    This Serializer provides Read functions for a CELL

"""
class CellSerializer(serializers.HyperlinkedModelSerializer):

    title = serializers.CharField(max_length=255, allow_blank=True)
    description = serializers.CharField(max_length=4095, allow_blank=True)
    column_index = serializers.IntegerField(source='xcoordinate')
    row_index = serializers.IntegerField(source='ycoordinate')
    cell_id = serializers.IntegerField(source='id')

    image = ImageSerializer(many=False, allow_null=True)

    class Meta:
        model = Cell
        fields = ('url', 'cell_id', 'title', 'description', 'column_index', 'row_index', 'image')
        read_only_fields = ('url', )



"""

    This Serializer provides Create, Read, Update and Delete functions for a Matrix (Bench)

"""
class MatrixSerializer(serializers.HyperlinkedModelSerializer):

    title = serializers.CharField(max_length=255, allow_blank=True)
    description = serializers.CharField(max_length=4095, allow_blank=True)
    height = serializers.IntegerField(default=75)
    width = serializers.IntegerField(default=75)

    owner = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    bench_cells = CellSerializer(many=True)

    class Meta:
        model = Matrix
        fields = ('url', 'id', 'title', 'description', 'height', 'width', 'owner', 'bench_cells')
        read_only_fields = ('id', 'url', )


    """
        Matrix Serializer, Create Method
    """
    def create(self, validated_data):
    
        #print("Bench Serializer, Create")

        matrix_title = validated_data.get('title')
        matrix_description = validated_data.get('description')
        matrix_height = validated_data.get('height')
        matrix_width = validated_data.get('width')
        matrix_owner = validated_data.get('owner')
        
        matrix_blogpost = 0

        self.validate_matrix_json_fields(matrix_title, matrix_description, matrix_height, matrix_width)

        cells_data = validated_data.pop('bench_cells')

        self.validate_cells(cells_data)

        matrix = Matrix.create(matrix_title, matrix_description, matrix_blogpost, matrix_height, matrix_width, matrix_owner)
        
        cell_list = list()

        for cell_data in cells_data:

            cell_title = cell_data.get('title')
            cell_description = cell_data.get('description')
            cell_xcoordinate = cell_data.get('xcoordinate')
            cell_ycoordinate = cell_data.get('ycoordinate')

            cell_blogpost = "0"

            image_data = cell_data.get('image')

            image = None
        
            if image_data is None:
        
                image = None

            else:
        
                image_active = False
                image_server = image_data.get('server')
                image_owner = image_data.get('owner')
                image_id = image_data.get('image_id')
                image_roi_id = image_data.get('roi')

                server = self.validate_image_json(image_server, image_owner, image_id, image_roi_id)
                
                image_identifier = int(image_id)

                image_name = ''
                image_viewer_url = ''
                image_birdseye_url = ''
                image_roi = 0
        
                if server.is_wordpress() == True:
        
                    data = server.check_wordpress_image(image_owner, image_id)
        
                    json_image = data['image']
            
                    image_name = json_image['name']
                    image_viewer_url = json_image['viewer_url']
                    image_birdseye_url = json_image['birdseye_url']
	        
                else:
        
                    data = server.check_imaging_server_image(image_owner, image_id)
        
                    json_image = data['image']
            
                    image_name = json_image['name']
                    image_viewer_url = json_image['viewer_url']
                    image_birdseye_url = json_image['birdseye_url']
            
                    if image_roi_id != 0:
                
                        data = server.check_imaging_server_image_roi(image_owner, image_id, image_roi_id)

                        json_roi = data['roi']
                
                        image_roi = int(json_roi['id'])
            

                if Image.objects.filter(Q(identifier=image_id) & Q(server=server) & Q(owner=image_owner) & Q(roi=image_roi) & Q(active=True)).exists():
            
                    #print("Image ALREADY Exists in Basket")
                    #print("UPDATE existing image")

                    existing_image_list = Image.objects.filter(Q(identifier=image_id) & Q(server=server) & Q(owner=image_owner) & Q(roi=image_roi) & Q(active=True))
                
                    image = existing_image_list[0]

                    image.active = False

                    image.save()
                
                else:
            
                    #print("Image DOES NOT Exist in Basket")
                    #print("No Previous Image, Create NEW image")
                
                    active = False
                
                    image = Image.create(image_id, image_name, server, image_viewer_url, image_birdseye_url, image_active, image_roi, image_owner)

                    image.save()
            
            cell_in = Cell.create(matrix, cell_title, cell_description, cell_xcoordinate, cell_ycoordinate, cell_blogpost, image)
            
            cell_list.append(cell_in)
        
        matrix.save()
        
        for cell_out in cell_list:
            
            cell_out.matrix = matrix

            cell_out.save()


        return matrix


    """
        Matrix Serializer, Update Method
    """
    def update(self, instance, validated_data):

        #print("Bench Serializer, Update")

        bench_title = validated_data.get('title', instance.title)
        bench_description = validated_data.get('description', instance.description)
        bench_height = validated_data.get('height', instance.height)
        bench_width = validated_data.get('width', instance.width)
        
        self.validate_matrix_json_fields(bench_title, bench_description, bench_height, bench_width)

        cells_data = validated_data.pop('bench_cells')
        
        self.validate_cells(cells_data)
        
        self.update_existing_cells(instance, cells_data)
        
        self.delete_missing_cells(instance, cells_data)

        self.add_new_cells(instance, cells_data)

        instance.title = bench_title
        instance.description = bench_description
        instance.height = bench_height
        instance.width = bench_width

        instance.save()

        return instance


    """
        Matrix Serializer, For a Matrix, Update any Existing Cells from Input Grid
    """
    def update_existing_cells(self, instance, cells_data):

        update_cell_list = list()    
        
        bench_cells = (instance.bench_cells).all()
        bench_cells = list(bench_cells)

        for bench_cell in bench_cells:
        
            bench_cell_id = bench_cell.id
            bench_cell_title = bench_cell.title
            bench_cell_description = bench_cell.description
            bench_cell_xcoordinate = bench_cell.xcoordinate
            bench_cell_ycoordinate = bench_cell.ycoordinate

            update_flag = True
            
            for cell_data in cells_data:
            
                cell_id = cell_data.get('id', 0)
                cell_title = cell_data.get('title')
                cell_description = cell_data.get('description')
                cell_xcoordinate = cell_data.get('xcoordinate')
                cell_ycoordinate = cell_data.get('ycoordinate')
                
                image_data = cell_data.get('image')

                if cell_id == bench_cell_id:
                
                    cell_image_data_id = 0
                    bench_image_data_id = 0
                    
                    if image_data is None:
                    
                        cell_image_data_id = 0
                    
                    else:
                    
                        cell_image_data_id = image_data.get('id')

                    if bench_cell.image is None:
                    
                        bench_image_data_id = 0
                        
                    else:
                        
                        bench_image_data_id = bench_cell.image.id

                    if cell_title == bench_cell_title and cell_description == bench_cell_description and cell_xcoordinate == bench_cell_xcoordinate and cell_ycoordinate == bench_cell_ycoordinate and cell_image_data_id == bench_image_data_id:

                        update_flag = False
                    
                    else:

                        bench_cell.title = cell_title
                        bench_cell.description = cell_description
                        bench_cell.xcoordinate = cell_xcoordinate
                        bench_cell.ycoordinate = cell_ycoordinate
                        
                        if image_data is not None and bench_cell.image is None:
                        
                            #update bench cell image with image_data
                            
                            image_active = False
                            image_server = image_data.get('server')
                            image_owner = image_data.get('owner')
                            image_id = image_data.get('image_id')
                            image_roi_id = image_data.get('roi')

                            server = self.validate_image_json(image_server, image_owner, image_id, image_roi_id)
                            
                            image_identifier = int(image_id)

                            image_name = ''
                            image_viewer_url = ''
                            image_birdseye_url = ''
                            image_roi = 0
        
                            if server.is_wordpress() == True:
        
                                data = server.check_wordpress_image(image_owner, image_id)
        
                                json_image = data['image']
            
                                image_name = json_image['name']
                                image_viewer_url = json_image['viewer_url']
                                image_birdseye_url = json_image['birdseye_url']
	        
                            else:
        
                                data = server.check_imaging_server_image(image_owner, image_id)
        
                                json_image = data['image']
            
                                image_name = json_image['name']
                                image_viewer_url = json_image['viewer_url']
                                image_birdseye_url = json_image['birdseye_url']
            
                                if image_roi_id != 0:
                            
                                    data = server.check_imaging_server_image_roi(image_owner, image_id, image_roi_id)

                                    json_roi = data['roi']
                            
                                    image_roi = int(json_roi['id'])
            

                            if Image.objects.filter(Q(identifier=image_id) & Q(server=server) & Q(owner=image_owner) & Q(roi=image_roi) & Q(active=True)).exists():
            
                                #print("Image ALREADY Exists in Basket")
                                #print("UPDATE existing image")

                                existing_image_list = Image.objects.filter(Q(identifier=image_id) & Q(server=server) & Q(owner=image_owner) & Q(roi=image_roi) & Q(active=True))
                            
                                image = existing_image_list[0]

                                image.active = False

                                image.save()
                            
                                bench_cell.image = image

                            else:
            
                                #print("Image DOES NOT Exist in Basket")
                                #print("No Previous Image, Create NEW image")
                            
                                active = False
                            
                                image = Image.create(image_id, image_name, server, image_viewer_url, image_birdseye_url, image_active, image_roi, image_owner)

                                image.save()
                                
                                bench_cell.image = image
                                

                        if image_data is not None and bench_cell.image is not None:
                        
                            #update bench cell image with image_data IF image_data is different
                            #    Set bench cell image Active to True
                            #    Set image data image Active to False

                            image_active = False
                            image_server = image_data.get('server')
                            image_owner = image_data.get('owner')
                            image_id = image_data.get('image_id')
                            image_roi_id = image_data.get('roi')

                            image_identifier = int(image_id)
                                
                            if image_identifier != bench_cell.image.identifier:

                                server = self.validate_image_json(image_server, image_owner, image_id, image_roi_id)
                                
                                image_name = ''
                                image_viewer_url = ''
                                image_birdseye_url = ''
                                image_roi = 0
        
                                if server.is_wordpress() == True:
        
                                    data = server.check_wordpress_image(image_owner, image_id)
        
                                    json_image = data['image']
            
                                    image_name = json_image['name']
                                    image_viewer_url = json_image['viewer_url']
                                    image_birdseye_url = json_image['birdseye_url']
	        
                                else:
        
                                    data = server.check_imaging_server_image(image_owner, image_id)
        
                                    json_image = data['image']
            
                                    image_name = json_image['name']
                                    image_viewer_url = json_image['viewer_url']
                                    image_birdseye_url = json_image['birdseye_url']
            
                                    if image_roi_id != 0:
                                
                                        data = server.check_imaging_server_image_roi(image_owner, image_id, image_roi_id)

                                        json_roi = data['roi']
                                
                                        image_roi = int(json_roi['id'])
            

                                if Image.objects.filter(Q(identifier=image_id) & Q(server=server) & Q(owner=image_owner) & Q(roi=image_roi) & Q(active=True)).exists():
            
                                    #print("Image ALREADY Exists in Basket")
                                    #print("UPDATE existing image")

                                    existing_image_list = Image.objects.filter(Q(identifier=image_id) & Q(server=server) & Q(owner=image_owner) & Q(roi=image_roi) & Q(active=True))
                                
                                    image = existing_image_list[0]

                                    image.active = False

                                    image.save()
                                
                                    old_image = bench_cell.image

                                    old_image.active = True
                                    
                                    old_image.save()
                                    
                                    bench_cell.image = image

                                else:
            
                                    #print("Image DOES NOT Exist in Basket")
                                    #print("No Previous Image, Create NEW image")
                                
                                    active = False
                                
                                    image = Image.create(image_id, image_name, server, image_viewer_url, image_birdseye_url, image_active, image_roi, image_owner)

                                    image.save()

                                    old_image = bench_cell.image

                                    old_image.active = True
                                    
                                    old_image.save()
                                    
                                    bench_cell.image = image


                        if image_data is None and bench_cell.image is not None:

                            #    Set bench cell image Active to True
                            
                            image = Image.objects.get(pk=bench_cell.image.id)
            
                            if image.active == False:
            
                                image.active = True
                                
                                image.save()
                            
                            bench_cell.image = None


                        update_cell_list.append(bench_cell)

            
        for update_cell in update_cell_list:
        
            update_cell.save()


    """
        Matrix Serializer, For a Matrix, Delete any Missing Cells from Input Grid
    """
    def delete_missing_cells(self, instance, cells_data):

        delete_cell_list = list()    
        
        bench_cells = (instance.bench_cells).all()
        bench_cells = list(bench_cells)

        for bench_cell in bench_cells:
        
            bench_cell_id = bench_cell.id

            delete_flag = True
            
            for cell_data in cells_data:
            
                cell_id = cell_data.get('id', 0)
                
                if cell_id == bench_cell_id:
                
                    delete_flag = False

            if delete_flag == True:
            
                delete_cell_list.append(bench_cell)

            
        for delete_cell in delete_cell_list:
        
            if delete_cell.image is not None:
            
                image = Image.objects.get(pk=delete_cell.image.id)
            
                if image.active == False:
            
                    image.active = True
                    image.save()

            delete_cell.delete()


    """
        Matrix Serializer, For a Matrix, Add New Cells
    """
    def add_new_cells(self, instance, cells_data):
    
        for cell_data in cells_data:

            cell_id = cell_data.get('id', 0)
            cell_title = cell_data.get('title')
            cell_description = cell_data.get('description')
            cell_xcoordinate = cell_data.get('xcoordinate')
            cell_ycoordinate = cell_data.get('ycoordinate')
            #cell_blogpost = cell_data.get('blogpost')
            cell_blogpost = "0"
            
            cell_image = None
                
            """
                Add NEW CELLS
            """
            if cell_id == 0:
            
                image_data = cell_data.pop('image')

                if image_data is None:
        
                    cell_image = None
                    
                else:

                    active = False
                    server = image_data.get('server')
                    owner = image_data.get('owner')
                    image_id = image_data.get('image_id')
                    roi_id = image_data.get('roi')

                    server = self.validate_image_json(server, owner, image_id, roi_id)
        
                    image_identifier = int(image_id)

                    image_name = ''
                    image_viewer_url = ''
                    image_birdseye_url = ''
                    image_roi = 0
        
                    if server.is_wordpress() == True:
        
                        data = server.check_wordpress_image(owner, image_id)
        
                        json_image = data['image']
                
                        image_name = json_image['name']
                        image_viewer_url = json_image['viewer_url']
                        image_birdseye_url = json_image['birdseye_url']
	        
                    else:
        
                        data = server.check_imaging_server_image(owner, image_id)
        
                        json_image = data['image']
                
                        image_name = json_image['name']
                        image_viewer_url = json_image['viewer_url']
                        image_birdseye_url = json_image['birdseye_url']
                
                        if roi_id != 0:
                    
                            data = server.check_imaging_server_image_roi(owner, image_id, roi_id)

                            json_roi = data['roi']
                    
                            image_roi = int(json_roi['id'])
                
                
                    if Image.objects.filter(Q(identifier=image_id) & Q(server=server) & Q(owner=owner) & Q(roi=image_roi) & Q(active=True)).exists():
                
                        #print("Image ALREADY Exists in Basket")
                        #print("UPDATE existing_image")

                        existing_image_list = Image.objects.filter(Q(identifier=image_id) & Q(server=server) & Q(owner=owner) & Q(roi=image_roi) & Q(active=True))
                    
                        existing_image = existing_image_list[0]

                        existing_image.active = False

                        existing_image.save()
                    
                        cell_image = existing_image

                    else:
                
                        #print("Image DOES NOT Exist in Basket")
                    
                        existing_image_list = Image.objects.filter(Q(identifier=image_id) & Q(server=server) & Q(owner=owner) & Q(roi=image_roi) & Q(active=False))
                    
                        existing_image = existing_image_list[0]

                        active = False

                        if existing_image.is_duplicate(image_id, image_name, server, image_viewer_url, image_birdseye_url, active, image_roi, owner) == True:
                    
                            #print("Attempting to Create NEW DUPLICATE of image")

                            cell_image = Image.create(image_id, image_name, server, image_viewer_url, image_birdseye_url, active, image_roi, owner)
                        
                            cell_image.save()
                        
                        else:

                            #print("No Previous Image, Create NEW image")

                            cell_image = Image.create(image_id, image_name, server, image_viewer_url, image_birdseye_url, active, image_roi, owner)
                        
                            cell_image.save()

                cell = Cell.create(instance, cell_title, cell_description, cell_xcoordinate, cell_ycoordinate, cell_blogpost, cell_image)
                
                cell.save()


    """
        Matrix Serializer, For a Matrix, Validate the supplied Title, Description, Height and Width fields
    """
    def validate_matrix_json_fields(self, title, description, height, width):
    
        len_title = len(title)
        len_description = len(description)
    
        """
            Title and Description field overflows are trapped by the Django REST framework, 
             so these next 2 checks are redundant
        """
        if len_title > 255:
                
            message = 'ERROR! Bench Title Length (' + str(len_title) + ') is greater than 255!'
            raise serializers.ValidationError(message)

        if len_description > 4095:
                
            message = 'ERROR! Bench Description Length (' + str(len_title) + ') is greater than 4095!'
            raise serializers.ValidationError(message)

        if height > 450:
                
            message = 'ERROR! Bench Cell Height (' + str(height) + ') is greater than 450!'
            raise serializers.ValidationError(message)

        if height < 75:
                
            message = 'ERROR! Bench Cell Height (' + str(height) + ') is less than 75!'
            raise serializers.ValidationError(message)
            
        if width > 450:
                
            message = 'ERROR! Bench Cell Width (' + str(width) + ') is greater than 450!'
            raise serializers.ValidationError(message)

        if width < 75:
                
            message = 'ERROR! Bench Cell Width (' + str(width) + ') is less than 75!'
            raise serializers.ValidationError(message)
            

    """
        Matrix Serializer, For a Matrix, Validate the supplied Cells
    """
    def validate_cells(self, cells_data):

        maxX = 0
        maxY = 0
        
        if not cells_data:
            message = 'ERROR! NO Cells supplied with Bench!'
            raise serializers.ValidationError(message)

        for cell_data in cells_data:
        
            title = cell_data.get('title')
            description = cell_data.get('description')
            
            self.validate_cell_json_fields(title, description)
            
            currX = int(cell_data.get('xcoordinate', 0))
            currY = int(cell_data.get('ycoordinate', 0))
            
            if currX > maxX:
                maxX = currX

            if currY > maxY:
                maxY = currY

        max_column_index = maxX
        max_row_index = maxY
        
        maxX += 1
        maxY += 1
        
        if maxX > 10:
            message = 'ERROR! Too many Columns in Bench (' + str(maxX) + '); No more than 10 Columns allowed!'
            raise serializers.ValidationError(message)

        if maxY > 10:
            message = 'ERROR! Too many Rows in Bench (' + str(maxY) + '); No more than 10 Rows allowed!'
            raise serializers.ValidationError(message)

        if maxX < 3:
            message = 'ERROR! Too few Columns in Bench (' + str(maxX) + '); At least 3 Columns required!'
            raise serializers.ValidationError(message)

        if maxY < 3:
            message = 'ERROR! Too few Rows in Bench (' + str(maxY) + '); At least 3 Rows required!'
            raise serializers.ValidationError(message)

        bench_cells=[[0 for cc in range(maxY)] for rc in range(maxX)]
        
        i = 0

        while i < maxX:
        
            j = 0
    
            while j < maxY:
            
                bench_cells[i][j] = False
                j += 1
            
            i += 1

        cnt = 0
        
        for cell_data in cells_data:
        
            cnt += 1
            
            i = cell_data.get('xcoordinate', 0)
            j = cell_data.get('ycoordinate', 0)
            
            if bench_cells[i][j] == True:
                message = 'ERROR! Duplicate Cell : Column Index = ' + str(i) + ', Row Index = ' + str(j)
                raise serializers.ValidationError(message)

            bench_cells[i][j] = True

        i = 0
        
        cnt = 0
        
        while i < maxX:
    
            j = 0
    
            while j < maxY:
            
                cnt += 1

                if bench_cells[i][j] == False:
                    message = 'ERROR! Missing Cell : Column Index = ' + str(i) + ', Row Index = ' + str(j)
                    raise serializers.ValidationError(message)

                j += 1
            
            i += 1


        for cell_data in cells_data:

            image_data = cell_data.get('image')
            
            xcoordinate = cell_data.get('xcoordinate', 0)
            ycoordinate = cell_data.get('ycoordinate', 0)
            
            if xcoordinate == 0 and image_data is not None:
                message = 'ERROR! An Image is not Permitted in : Column Index = ' + str(xcoordinate)
                raise serializers.ValidationError(message)

            if xcoordinate == max_column_index and image_data is not None:
                message = 'ERROR! An Image is not Permitted in : Column Index = ' + str(xcoordinate)
                raise serializers.ValidationError(message)

            if ycoordinate == 0 and image_data is not None:
                message = 'ERROR! An Image is not Permitted in : Row Index = ' + str(ycoordinate)
                raise serializers.ValidationError(message)

            if ycoordinate == max_row_index and image_data is not None:
                message = 'ERROR! An Image is not Permitted in : Row Index = ' + str(ycoordinate)
                raise serializers.ValidationError(message)

            if image_data is not None:
        
                active = False
                server = image_data.get('server')
                owner = image_data.get('owner')
                image_id = image_data.get('image_id')
                roi_id = image_data.get('roi')

                server = self.validate_image_json(server, owner, image_id, roi_id)


        return True


    """
        Matrix Serializer, For a Cell in a Matrix, Validate the supplied Title and Description fields
    """
    def validate_cell_json_fields(self, title, description):
    
        len_title = len(title)
        len_description = len(description)
    
        """
            Title and Description field overflows are trapped by the Django REST framework, 
             so these next 2 checks are redundant
        """
        if len_title > 255:
                
            message = 'ERROR! Cell Title Length (' + str(len_title) + ') is greater than 255!'
            raise serializers.ValidationError(message)

        if len_description > 4095:
                
            message = 'ERROR! Cell Description Length (' + str(len_title) + ') is greater than 4095!'
            raise serializers.ValidationError(message)


    """
        Matrix Serializer, For an Image in a Cell within a Matrix, Validate the supplied Server, Owner, Image Id and ROI ID Fields
    """
    def validate_image_json(self, server_str, user, image_id, roi_id):
    
        server_list = server_str.split("@")
        
        server_uid = str(server_list[0])
        server_url = str(server_list[1])
        
        if Server.objects.filter(Q(uid=server_uid) & Q(url_server=server_url)).exists():

            server = Server.objects.get(Q(uid=server_uid) & Q(url_server=server_url))
            
            if server.is_wordpress() == True:
                
                if self.validate_wordpress_image_id(server, user, image_id) == False:

                    message = 'ERROR! Image NOT Present on : ' + server_str
                    raise serializers.ValidationError(message)
            else:

                if server.is_omero547() == True or server.is_omero56() == True:

                    if self.validate_imaging_image_id(server, user, image_id) == True:
                
                        if roi_id != 0:
                    
                            if self.validate_roi_id(server, user, image_id, roi_id) == False:
                            
                                message = 'ERROR! ROI ID ' + str(roi_id) + ', for Image ID ' + str(image_id) + ", NOT Present on : " + server_str
                                raise serializers.ValidationError(message)
                    else:

                        message = 'ERROR! Image ID ' + str(image_id) + ', NOT Present on : ' + server_str
                        raise serializers.ValidationError(message)
                else:

                    message = 'ERROR! Server Type Unknown : ' + server_str
                    raise serializers.ValidationError(message)
            
            return server

        else:

            message = 'ERROR! Server Unknown : ' + server_str
            raise serializers.ValidationError(message)
            
            return None


    """
        Matrix Serializer, For an Image in a Cell within a Matrix, Validate the supplied Server, Owner, Image Id and ROI ID Fields
    """
    def validate_wordpress_image_id(self, server, user, image_id):
    
        data = server.check_wordpress_image(user, image_id)
        
        image_name = data['name']

        if image_name == "":
            return False
        else:
            return True


    """
        Matrix Serializer, For an OMERO Image in a Cell within a Matrix, Check the supplied Image Exists
    """
    def validate_imaging_image_id(self, server, user, image_id):
    
        data = server.check_imaging_server_image(user, image_id)
        
        json_image = data['image']
        image_name = json_image['name']
        
        if image_name == "":
            return False
        else:
            return True


    """
        Matrix Serializer, For an OMERO Image in a Cell within a Matrix, Check the supplied Image ROI ID Exists
    """
    def validate_roi_id(self, server, user, image_id, roi_id):
    
        data = server.check_imaging_server_image_roi(user, image_id, roi_id)

        json_roi = data['roi']
        roi_id = json_roi['id']

        if roi_id == "":
            return False
        else:
            return True
