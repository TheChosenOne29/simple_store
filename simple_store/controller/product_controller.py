import json
from pyramid.view import view_config, view_defaults
from pyramid.response import Response
from pyramid.request import Request
from sqlalchemy.exc import DBAPIError
from ..models import Product

@view_defaults(route_name="product")
class ProductView:
    def __init__(self, request):
        self.request: Request = request

    @view_config(request_method="GET")
    def read(self):
        try:
            products = self.request.dbsession.query(Product).all()
            return Response(
                json={
                    "data": [
                        {
                            "id": item.id,
                            "name": item.name,
                            "price": item.price,
                        }
                        for item in products
                    ]
                },
                status=200,
                content_type="application/json",
            )
        except DBAPIError:
            return Response(
                json=json.dumps({"message": "failed"}),
                status=500,
                content_type="application/json",
            )
            
    @view_config(request_method="POST")
    def create(self):
        try:
            try:
                name = self.request.json_body["name"]
                price = self.request.json_body["price"]
                desc = self.request.json_body["desc"]
            except:
                return Response(
                    content_type="application/json",
                    charset="UTF-8",
                    status=400,
                    body=json.dumps({"error": "Title or content is empty!"}),
                )

            products = Product(name = name, price = price, desc = desc)
            self.request.dbsession.add(products)
            self.request.dbsession.flush()
            
            product_data = {
            "name": products.name,
            "price": products.price,
            "desc": products.desc,
        }

            return Response(
                json={"message": "success", "data" : product_data},
                status=200,
                content_type="application/json",
            )

        except DBAPIError:
            return Response(
                json={"message": "failed"},
                status=500,
                content_type="application/json",
            )

    @view_config(request_method="PUT")
    def update(self):
        try:
            try:
                id = self.request.json_body["id"]
                name = self.request.json_body["name"]
                price = self.request.json_body["price"]
                desc = self.request.json_body["desc"]
            except:
                return Response(
                    content_type="application/json",
                    charset="UTF-8",
                    status=400,
                    body=json.dumps({"error": "ID, title or content is empty!"}),
                )

            products = self.request.dbsession.query(Product).filter_by(id=id).first()

            products.name = name
            products.price = price
            products.desc = desc

            self.request.dbsession.flush()

            return Response(
                json={"message": "success"},
                status=201,
                content_type="application/json",
            )
        except DBAPIError:
            return Response(
                json={"message": "failed"},
                status=500,
                content_type="application/json",
            )

    @view_config(request_method="DELETE")
    def delete(self):
        try:
            try:
                id = self.request.json_body["id"]
            except:
                return Response(
                    content_type="application/json",
                    charset="UTF-8",
                    status=400,
                    body=json.dumps({"error": "ID is empty!"}),
                )

            products = self.request.dbsession.query(Product).filter_by(id=id).first()
            self.request.dbsession.delete(products)
            self.request.dbsession.flush()

            return Response(
                json={"message": "success"},
                status=200,
                content_type="application/json",
            )
        except DBAPIError:
            return Response(
                json={"message": "failed"},
                status=500,
                content_type="application/json",
            )
