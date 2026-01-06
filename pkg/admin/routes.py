from flask import render_template
from pkg.admin import adminobj
from pkg.models import db, State, City


NIGERIA_LOCATIONS = {
    "Abia": ["Aba", "Umuahia", "Ohafia", "Arochukwu"],
    "Adamawa": ["Yola", "Mubi", "Numan", "Ganye"],
    "Akwa Ibom": ["Uyo", "Ikot Ekpene", "Eket", "Oron"],
    "Anambra": ["Awka", "Onitsha", "Nnewi", "Ekwulobia"],
    "Bauchi": ["Bauchi", "Azare", "Misau", "Jama’are"],
    "Bayelsa": ["Yenagoa", "Ogbia", "Brass", "Nembe"],
    "Benue": ["Makurdi", "Gboko", "Otukpo", "Katsina-Ala"],
    "Borno": ["Maiduguri", "Biu", "Dikwa", "Gwoza"],
    "Cross River": ["Calabar", "Ikom", "Ogoja", "Obudu"],
    "Delta": ["Asaba", "Warri", "Sapele", "Ughelli"],
    "Ebonyi": ["Abakaliki", "Afikpo", "Onueke"],
    "Edo": ["Benin City", "Auchi", "Ekpoma"],
    "Ekiti": ["Ado-Ekiti", "Ikere", "Omuo"],
    "Enugu": ["Enugu", "Nsukka", "Awgu", "Udi"],
    "Gombe": ["Gombe", "Kaltungo", "Dukku"],
    "Imo": ["Owerri", "Orlu", "Okigwe"],
    "Jigawa": ["Dutse", "Hadejia", "Gumel"],
    "Kaduna": ["Kaduna", "Zaria", "Kafanchan"],
    "Kano": ["Kano", "Wudil", "Rano", "Gaya"],
    "Katsina": ["Katsina", "Daura", "Funtua"],
    "Kebbi": ["Birnin Kebbi", "Argungu", "Yauri"],
    "Kogi": ["Lokoja", "Okene", "Idah"],
    "Kwara": ["Ilorin", "Offa", "Omu-Aran"],
    "Lagos": ["Ikeja", "Lekki", "Yaba", "Surulere", "Ikorodu", "Badagry"],
    "Nasarawa": ["Lafia", "Keffi", "Akwanga"],
    "Niger": ["Minna", "Bida", "Suleja"],
    "Ogun": ["Abeokuta", "Ijebu-Ode", "Ota", "Sagamu"],
    "Ondo": ["Akure", "Owo", "Ondo", "Ikare"],
    "Osun": ["Osogbo", "Ile-Ife", "Ilesa"],
    "Oyo": ["Ibadan", "Ogbomosho", "Oyo", "Iseyin"],
    "Plateau": ["Jos", "Bukuru", "Pankshin"],
    "Rivers": ["Port Harcourt", "Obio-Akpor", "Bonny", "Ahoada"],
    "Sokoto": ["Sokoto", "Wamako", "Tambuwal"],
    "Taraba": ["Jalingo", "Wukari", "Takum"],
    "Yobe": ["Damaturu", "Potiskum", "Gashua"],
    "Zamfara": ["Gusau", "Kaura Namoda", "Talata Mafara"],
    "FCT": ["Abuja", "Garki", "Wuse", "Maitama", "Kubwa"]
}





@adminobj.route('/')
def home():
    return render_template('admin/index.html')


@adminobj.route('/dashboard/')
def dashboard():
    return render_template('admin/dashboard.html')


@adminobj.route('/create/states-cities')
def create_states_cities():
    """
    Admin route to seed Nigerian states and their cities
    """
    for state_name, cities in NIGERIA_LOCATIONS.items():
        # Check if state already exists
        state = State.query.filter_by(name=state_name).first()
        if not state:
            state = State(name=state_name)
            db.session.add(state)
            db.session.flush()  # make state.id available

        # Add cities
        for city_name in cities:
            exists = City.query.filter_by(name=city_name, state_id=state.id).first()
            if not exists:
                db.session.add(City(name=city_name, state_id=state.id))

    db.session.commit()
    return "Nigerian states and cities created successfully!"



