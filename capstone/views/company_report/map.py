from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import pandas as pd
import sqlite3 as sql
import folium
from folium import plugins
from folium.plugins import MarkerCluster
from capstone.models import Customer
import geopandas as gpd
import matplotlib.pyplot as plt
import pickle
import seaborn as sns


def create_map(id_for_map):
    conn = sql.connect("db.sqlite3")
    pay_df = pd.read_sql_query("SELECT * FROM capstone_payment;", conn)

    cust_df = pd.read_sql_query("SELECT * FROM capstone_customer;", conn)

    payment_zipcode = pd.merge(pay_df, cust_df, left_on="customer_id", right_on="id")

    card_df = pd.read_sql_query("SELECT * FROM capstone_giftcard;", conn)

    company_df = pd.read_sql_query("SELECT * FROM capstone_company;", conn)

    company_card_df = pd.merge(card_df, company_df, left_on="company_id", right_on="id")

    payment_company_zip_df = pd.merge(payment_zipcode, company_card_df, left_on="giftcard_id", right_on="id_x")

    final_df = payment_company_zip_df[['payment_date', 'amount_donated', 'zipcode', 'id_y_y', 'name']]
    final_df = final_df.rename(columns={'id_y_y': 'company_id'})
    final_df = final_df[final_df.company_id==int(id_for_map)]
    final_df = final_df.groupby("zipcode")["amount_donated"].sum().reset_index()

    geo_df = pd.read_json("./data2.0/USCities.json", orient="records")

    my_crs = "{'init': 'epsg:4326'}"

    zipcodes_pickle = pd.read_pickle("./data2.0/zipcodes.pickle")
    zipcodes_pickle_gdf = gpd.GeoDataFrame(zipcodes_pickle, crs=my_crs, geometry=zipcodes_pickle.geometry)

    geo_df = geo_df[['latitude', 'longitude', 'zip_code', 'city']]

    latt_long_df = pd.merge(final_df, geo_df, left_on="zipcode", right_on="zip_code")

    my_zips = list(latt_long_df.zipcode.astype("str").values)
    filtered_zips = zipcodes_pickle_gdf.loc[zipcodes_pickle_gdf["ZCTA5CE10"].isin(my_zips)]
    filtered_zips["ZCTA5CE10"] = filtered_zips["ZCTA5CE10"].astype("int")
    final_zip_area = pd.merge(filtered_zips, latt_long_df[["zipcode", "amount_donated"]], left_on="ZCTA5CE10", right_on="zipcode")

    quantiles = 10
    final_zip_area['quantile'] = pd.qcut(final_zip_area['amount_donated'], quantiles, labels=False)
    colors = sns.color_palette("Reds_r", int(1.25*quantiles)).as_hex()
    final_zip_area['style'] = final_zip_area['quantile'].apply(
    lambda l: {
        'fillColor': colors[quantiles-1-int(l)],
        'fillOpacity': 0.9,})

    base_map = folium.Map(location=[37.0902, -95.7129], control_scale=True, zoom_start=4.5)

    for i in range(len(final_zip_area)):
        gs = folium.GeoJson(final_zip_area.iloc[i:i+1])
        label = '{}: ${}'.format(
            final_zip_area['zipcode'][i], str(round(float(final_zip_area['amount_donated'][i]), 2)))
        folium.Popup(label).add_to(gs)
        gs.add_to(base_map)

    mc = MarkerCluster()
    for idx,row in latt_long_df.iterrows():
        mc.add_child(folium.Marker(location=[row.latitude,  row.longitude], popup=f"{row.zipcode}: ${str(round(float(row.amount_donated), 2))}"))

    base_map.add_child(mc)


    base_map.save('capstone/templates/report/gift_cards.html')


@login_required
def Map(request):
    customer = Customer.objects.get(pk=request.user.id)
    create_map(customer.company.id)
    if request.method == 'GET':
        template_name = 'report/gift_cards.html'
        return render(request, template_name, {})