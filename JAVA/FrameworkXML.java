//Program to implement iCRUD

import java.io.File;
import java.io.FileWriter;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import org.w3c.dom.Attr;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import java.util.Scanner;
import org.json.simple.JSONObject;
import org.json.simple.JSONArray;

class XML implements iCRUD
{
    SQLParser objSQLParser;
    File file;
    DocumentBuilderFactory dbf;
    DocumentBuilder db;
    Document document;
    Element root;
    String[] fieldNames;
    String[] fieldValues;
    String tableName;

    public XML() throws Exception
    {
    	file = new File("Data.xml");
    	objSQLParser = new SQLParser();
        dbf = DocumentBuilderFactory.newInstance();  
        db = dbf.newDocumentBuilder();  
        document = db.parse(file);  
        document.getDocumentElement().normalize();
        root = document.getDocumentElement();
        fieldNames = getFieldNames();
    }

    public int insertRecord(String query) throws Exception
    {
        fieldValues = objSQLParser.getColumnValues(query);
        tableName = objSQLParser.getTableName(query);
	    Element child = document.createElement(tableName);
        root.appendChild(child);
        Attr attr = document.createAttribute("Status");
        attr.setValue("A");
        child.setAttributeNode(attr);
        for(int index = 0; index < fieldNames.length; index++)
        {
            Element subChild = document.createElement(fieldNames[index]);
            subChild.appendChild(document.createTextNode(fieldValues[index]));
            child.appendChild(subChild);
        }
        return writeRecords();
    }

    public JSONObject readRecords(String query) throws Exception
    {
    	tableName = objSQLParser.getTableName(query);
        NodeList nList = getNodeList(tableName);
        JSONObject objJSON = new JSONObject();
		JSONArray array = new JSONArray();
        for (int index = 0; index < nList.getLength(); index++) 
        {
        	Node nNode = nList.item(index);
        	Element eElement = (Element) nNode;
        	String attribute = eElement.getAttribute("Status");
        	if(attribute.equals("A"))
        	{
        		JSONObject record = new JSONObject();
        		NodeList childNodes = nNode.getChildNodes();
	        	for(int childNodesIndex = 0; childNodesIndex < childNodes.getLength(); childNodesIndex++)
	        	{
	        		Node node = childNodes.item(childNodesIndex);
	        		record.put(node.getNodeName(), node.getTextContent());
	        	}
	        	array.add(record);
        	}
        }
        objJSON.put(tableName, array);
		return objJSON;
    }

    public JSONObject searchRecord(String query) throws Exception
    {
    	fieldValues = objSQLParser.getColumnValues(query);
    	tableName = objSQLParser.getTableName(query);
		JSONObject objJSON = new JSONObject();
		JSONArray array  = new JSONArray();
    	NodeList nList = getNodeList(tableName);
        for (int index = 0; index < nList.getLength(); index++) 
        {
        	Node nNode = nList.item(index);
        	Element eElement = (Element) nNode;
        	String attribute = eElement.getAttribute("Status");
        	String id = eElement.getElementsByTagName(fieldNames[0]).item(0).getTextContent();
        	if(attribute.equals("A") && id.equals(fieldValues[1]))
        	{
				JSONObject record = new JSONObject();
	        	for(int fieldNamesIndex= 0; fieldNamesIndex < fieldNames.length; fieldNamesIndex++)
	        	{
	        		record.put(fieldNames[fieldNamesIndex], eElement.getElementsByTagName(fieldNames[fieldNamesIndex]).item(0).getTextContent());
	        	}
	        	array.add(record);
	    		objJSON.put(tableName, array);
	        	break;
        	}
        }
		return objJSON;
    }	

    public int deleteRecord(String query) throws Exception
    {
    	fieldValues = objSQLParser.getColumnValues(query);
    	tableName = objSQLParser.getTableName(query);
    	NodeList nList = getNodeList(tableName);
    	int deleteRecordStatus = 0;
        for (int index = 0; index < nList.getLength(); index++) 
        {
        	Node nNode = nList.item(index);
        	Element eElement = (Element) nNode;
        	String attribute = eElement.getAttribute("Status");
        	String id = eElement.getElementsByTagName(fieldNames[0]).item(0).getTextContent();
        	if(attribute.equals("A") && id.equals(fieldValues[1]))
        	{
	        	eElement.setAttribute("Status", "D");
	        	deleteRecordStatus = writeRecords();
	        	break;
        	}
        }
        return deleteRecordStatus;
    }

    public int updateRecord(String query) throws Exception
    {
    	fieldValues = objSQLParser.getColumnValues(query);
    	String[] updatableFieldNames = objSQLParser.getColumnNames(query);
    	int updateRecordStatus = 0;
    	tableName = objSQLParser.getTableName(query);
    	NodeList nList = getNodeList(tableName);
        for (int index = 0; index < nList.getLength(); index++) 
        {
        	Node nNode = nList.item(index);
        	Element eElement = (Element) nNode;
        	String attribute = eElement.getAttribute("Status");
        	String id = eElement.getElementsByTagName(fieldNames[0]).item(0).getTextContent();
        	if(attribute.equals("A") && id.equals(fieldValues[1]))
        	{
        		NodeList nodes = nNode.getChildNodes();
        		for(int rowIndex = 0; rowIndex < nodes.getLength(); rowIndex++)
        		{
        			Node node = nodes.item(rowIndex);
        			if (updatableFieldNames[0].equals(node.getNodeName()))
        			{
        				node.setTextContent(fieldValues[0]);
        				updateRecordStatus = writeRecords();
        				break;
        			}
        		}

        	}
        }
        return updateRecordStatus;
    }

    public NodeList getNodeList(String tagName)
    {
    	NodeList nList = document.getElementsByTagName(tagName);
    	return nList;
    }

    public String[] getConfigData(String fileName) throws Exception
    {
    	String configData = "";
    	try 
    	{
			File myObj = new File(fileName + ".cfg");
			Scanner scanner = new Scanner(myObj);  
			while (scanner.hasNextLine()) 
			{
				configData = scanner.nextLine();
			}
			scanner.close();
		}
		catch (Exception e)
		{
			System.out.println("An error occurred.");
			e.printStackTrace();
		}
        return configData.split(", ");
    }

    public int writeRecords()
    {
    	try
    	{
	    	TransformerFactory transformerFactory = TransformerFactory.newInstance();
	        Transformer transformer = transformerFactory.newTransformer();
	        DOMSource domSource = new DOMSource(document);
	        StreamResult streamResult = new StreamResult(new FileWriter(file));
	        transformer.transform(domSource, streamResult);
	        return 1;
    	}
    	catch (Exception objException)
    	{
    		return 0;
    	}
    }

    public String[] getFieldNames()
    {
    	String data = "";
    	try 
    	{
			File myObj = new File("FieldNames.cfg");
			Scanner scanner = new Scanner(myObj);  
			while (scanner.hasNextLine()) 
			{
				data = scanner.nextLine();
			}
			scanner.close();
		}
		catch (Exception e)
		{
			System.out.println("An error occurred.");
			e.printStackTrace();
		}
		return data.split(", ");
	}
}


