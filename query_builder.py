def build_es_query(degree=None, skills=None, title=None, career_level=None):
    """Builds an ES query based on specified input"""

    # Match all if no input provided
    if not degree and not skills and not title and not career_level:
        query = {
            "query": {
                "match_all": {}
            }
        }

    # Create custom query
    else:
        query = {
            "query": {
                "bool": {
                    "must": [
                    ]
                }
            }
        }
        must = query["query"]["bool"]["must"]

        # Match against strings
        if degree:
            must.append({"nested":{"path":"education","query":{"match":{"education.degree":{"query":degree,"fuzziness":"AUTO"}}}}})
        if title:
            must.append({"nested":{"path":"experience","query":{"match":{"experience.title":{"query":title,"fuzziness":"AUTO"}}}}})

        # Wildcard match against any provided skills
        if skills:
            query["query"]["bool"]["should"] = [{"wildcard": {"skills": f"*{skill}*"}} for skill in skills]
            query["query"]["bool"]["minimum_should_match"] = 1

        # Use years_experience to select a career level
        if career_level:
            if career_level == "entry":
                must.append({"range": {"years_experience": {"lte": 2}}})
            elif career_level == "mid":
                must.append({"range": {"years_experience": {"gte": 3, "lte": 7}}})
            elif career_level == "senior":
                must.append({"range": {"years_experience": {"gte": 8}}})

    return query
