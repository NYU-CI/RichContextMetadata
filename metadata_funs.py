import dimensions_search_api_client as dscli
import time

def connect_ds_api(username,password):
    api_client = dscli.DimensionsSearchAPIClient()
    api_client.set_max_in_items( 100 )
    api_client.set_max_return( 1000 )
    api_client.set_max_overall_returns( 50000 )
    api_client.set_username( username )
    api_client.set_password( password )
    return api_client

def run_string_search(string,api_client):
    search_string = 'search publications in full_data for "{}" return publications'.format(string)
    api_response = api_client.execute_query(query_string_IN = search_string )
    return api_response


def run_exact_string_search(string,api_client):
    search_string = 'search publications in full_data for "\\"{}\\"" return publications'.format(string)
    api_response = api_client.execute_query(query_string_IN = search_string )
    return api_response

def run_doi_search(doi_id,api_client):
    doi_search_string = 'search publications where doi = "{}" return publications[all] limit 1'.format(doi_id)
    doi_response = api_client.execute_query( query_string_IN=doi_search_string )
    publication_metadata = doi_response['publications'][0]
    return publication_metadata


def run_pub_id_search(dimensions_id,api_client):
    id_search_string = 'search publications where id = "{}" return publications[all] limit 1'.format(dimensions_id)
    id_response = api_client.execute_query( query_string_IN=id_search_string )
    publication_metadata = id_response['publications'][0]
    return publication_metadata

def return_string_search_dyads(exact_match: bool, dataset_string: str, api_client):
    if exact_match == True:
        api_return = run_exact_string_search(string = dataset_string, api_client = api_client)
    if exact_match == False:
        api_return = run_string_search(string = dataset_string, api_client = api_client)
    pub_metadata = []
    for i in api_return['publications']:
        time.sleep( 6 )
        try:
            pub_id = i['id']
            id_metadata = run_pub_id_search(dimensions_id = pub_id, api_client = api_client)
            try:
                doi_id = id_metadata['doi']
            except:
                doi_id = None
            id_metadata.update({'dataset_name':dataset_string})
            pub_metadata.append(id_metadata)
        except Exception as e:               
            print("Could not fetch metadata for publication: {}".format(doi_id))
    return pub_metadata

def flatten(l):
    flat_list = [item for sublist in l for item in sublist]
    return flat_list


def run_author_search(author_dimensions_id, api_client):
    auth_query = 'search researchers where id = "{}" return researchers[all]'.format(author_dimensions_id)
    author_return = api_client.execute_query( query_string_IN=auth_query )
    author_metadata = author_return['researchers']
    return author_metadata