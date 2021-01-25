from blueprints import db
from blueprints.admin.model import Admin
from blueprints.category.model import Category
from blueprints.product.model import Product
from blueprints.user.model import User

def seeder():
    # Create Admin
    admin_seed()
    print('Admin Seed OK')
    
    # Create Category
    category_seed()
    print('Category Seed OK')

    # Create Product
    product_seed()
    print('Product Seed Ok')

    # Create User
    user_seed()
    print('User seed OK')

def admin_seed():
    try:
        new_admin = Admin('admin', 'admin', 1)
        new_admin_2 = Admin('adminbiasa', 'adminbiasa', 0)

        admin_query = Admin.query.all()

        if len(admin_query) == 0:
            db.session.add(new_admin)
            db.session.commit()
            print('Add a Admin -> Id: admin, Pass: admin, status: SuperAdmin')
    
            db.session.add(new_admin_2)
            db.session.commit()
            print('Add a Admin -> Id: adminbiasa, Pass: adminbiasa, status: NonSuperAdmin')
    
    except Exception as e:
        print(e)


def category_seed():
    try:
        shirt_category = Category('Shirt', 'Shirt')

        category_query = Category.query.all()

        if len(category_query) == 0:            
            db.session.add(shirt_category)
            db.session.commit()
            print('Add Category Shirt')
        
    except Exception as e:
        print(e)

def product_seed():
    try:
        black_shirt_product = Product(1, 2, 'Black Shirt', 100, 50000, 500, 'https://cf.shopee.co.id/file/597343d149e477b96465773b464509e8', 'Kemeja Hitam Berkualitas')
        red_shirt_product = Product(1, 2, 'Red Shirt', 100, 50000, 500, 'https://cf.shopee.co.id/file/711234d4eecc4236526b67f379a72a51', 'Kaos Merah Berkualitas')
        
        product_query = Product.query.all()

        if len(product_query) == 0:
            db.session.add(black_shirt_product)
            db.session.commit()
            print('Add Product Black Shirt')

            db.session.add(red_shirt_product)
            db.session.commit()
            print('Add Product Red Shirt')


    except Exception as e:
        print(e)

def user_seed():
    try:
        new_user = User('user', 'user', 'user@user.com')
        new_user2 = User('userbaru', 'userbaru', 'userbaru@userbaru.com')

        user_query = User.query.all()

        if len(user_query) == 0:
            db.session.add(new_user)
            db.session.commit()
            db.session.add(new_user2)
            db.session.commit()
            print('Add user')

    except Exception as e:
        print(e)