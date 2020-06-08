#!/usr/bin/python3
from models.comunas import Comunas
from models.reports import Reports
from models.mapping import Mapping
from models.collective_group import Collectivegroup
from models.stage import Stage
from models.neighborhood import Neighborhood

class Stadistics:

    @classmethod
    def stadisticsByComuna(cls, idComuna):
        """
        """
        results = {
            "total_cases": 0,
            "total_complaint": 0,
            "stages": {},
            "neighborhood": {},
            "collective": {},
        }
        
        if Comunas.validComuna(idComuna):
            neighborhoods = {}
            for item in Neighborhood.readAll().values():
                if item.get("idComuna") == idComuna:
                    item["cases"] = 0
                    del item["idComuna"]
                    neighborhoods[item.get("idNeighborhood")] = item

            dataStage = {}
            for item in Stage.readAll().values():
                item["cases"] = 0
                dataStage[item.get("idStages")] = item

            collective = {}
            for item in Collectivegroup.readAll().values():
                item["cases"] = 0
                collective[item.get("idCollective")] = item

            # cases by neighborhood
            for item in Reports.readAll().values():
                if item.get("idNeighborhood") in neighborhoods.keys():                    
                    neighborhoods[item.get("idNeighborhood")]["cases"] = neighborhoods[item.get("idNeighborhood")]["cases"] + 1
                    dataStage[item.get("idStage")]["cases"] = dataStage[item.get("idStage")]["cases"] + 1
                    collective[item.get("idCollective")]["cases"] = collective[item.get("idCollective")]["cases"] + 1
                    results["total_cases"] = results["total_cases"] + 1

                if item.get("complaint") != "No":
                    results["total_cases"] = results["total_cases"] + 1

            copy = dataStage.copy()
            for key, value in copy.items():
                if value.get("cases") == 0:
                    del dataStage[key]

            copy = neighborhoods.copy()
            for key, value in copy.items():
                if value.get("cases") == 0:
                    del neighborhoods[key]

            copy = collective.copy()
            for key, value in copy.items():
                if value.get("cases") == 0:
                    del collective[key]

            results["stages"] = dataStage
            results["neighborhood"] = neighborhoods
            results["collective"] = collective
        return results
