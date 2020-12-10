// Program to parse the given SQL query

class SQLParser
{

	public String getTableName(String query)
	{
		String properSpacedQuery = removeExtraSpaces(query);
		String[] parsedQuery = properSpacedQuery.split(" ");
		if (parsedQuery[0].toUpperCase().equals("SELECT"))
		{
			for (int index = 1; index < parsedQuery.length; index++)
			{
				if (parsedQuery[index].toUpperCase().equals("FROM"))
				{
					return parsedQuery[index + 1];
				}
			}
		}
		else if(parsedQuery[0].toUpperCase().equals("INSERT"))
		{
			return parsedQuery[2];
		}
		else if(parsedQuery[0].toUpperCase().equals("UPDATE"))
		{
			return parsedQuery[1];
		}

		return "";
	}

	public String[] getColumnNames(String query)
	{
		String fieldNames = "";
		String properSpacedQuery = removeExtraSpaces(query);
		String replacedQuery = properSpacedQuery.replaceAll("[(,)]", "");
		String[] parsedQuery = replacedQuery.split(" ");
		if(parsedQuery[0].toUpperCase().equals("INSERT"))
		{
			for (int index = 3; index < parsedQuery.length; index++)
			{
				if (parsedQuery[index].toUpperCase().equals("VALUES") != true)
				{
					fieldNames += parsedQuery[index] + " ";
				}
				else
				{
					break;
				}
			}
		}
		else if(parsedQuery[0].toUpperCase().equals("UPDATE"))
		{
			fieldNames += parsedQuery[3] + " " + parsedQuery[7];
		}
		else if(parsedQuery[0].toUpperCase().equals("SELECT"))
		{
			for (int index = 1; index < parsedQuery.length; index++)
			{
				if (parsedQuery[index].toUpperCase().equals("WHERE"))
				{
					index += 1;
					fieldNames += parsedQuery[index] + " ";
					while (index + 2 != parsedQuery.length - 1)
					{
						index += 4;
						fieldNames += parsedQuery[index] + " ";
					}
					break;
				}
				
			}			
		}
		return fieldNames.split(" ");
	}

	public String[] getColumnValues(String query)
	{
		String fieldValues = "";
		String properSpacedQuery = removeExtraSpaces(query);
		String replacedQuery = properSpacedQuery.replaceAll("[(,\')]", "");
		String[] parsedQuery = replacedQuery.split(" ");
		if(parsedQuery[0].toUpperCase().equals("INSERT"))
		{
			int counter = 0;
			for (int index = 3; index < parsedQuery.length; index++)
			{
				if (parsedQuery[index].toUpperCase().equals("VALUES"))
				{
					counter = index;
				}
				else if(index > counter && counter != 0)
				{
					fieldValues += parsedQuery[index] + " ";
				}
			}
		}
		else if(parsedQuery[0].toUpperCase().equals("UPDATE"))
		{
			fieldValues += parsedQuery[5] + " " + parsedQuery[9];
		}
		else if(parsedQuery[0].toUpperCase().equals("SELECT"))
		{
			for (int index = 1; index < parsedQuery.length; index++)
			{
				if (parsedQuery[index].toUpperCase().equals("WHERE"))
				{
					index += 3;
					fieldValues += parsedQuery[index] + " ";
					while (index != parsedQuery.length - 1)
					{
						index += 4;
						fieldValues += parsedQuery[index] + " ";
					}
					break;
				}
			}			
		}
		return fieldValues.split(" ");
	}

	public String removeExtraSpaces(String query)
	{
		return query.trim().replaceAll("[ ]{2,}", " "); 
	}
}