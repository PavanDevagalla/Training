// Program to use CRUDMySQL library

using System;
using MySQLLib;
using System.Data.Common;
using System.Data;

class MySqlMain
{
	static String[] FieldNames;
	static CRUDMySQL ObjCRUD;
	public static void Main(String[] args)
	{
		ObjCRUD = new CRUDMySQL();
		FieldNames = ObjCRUD.GetFieldNames();
		InsertRecord();
		Console.WriteLine("------------------------");
		ReadRecords();
	}

	public static void InsertRecord()
	{
		String Query = "INSERT INTO MyTable VALUES (";
		for (int Index = 0; Index < FieldNames.Length; Index++)
		{
			Console.Write(FieldNames[Index] + ": ");
			Query += "'" + Console.ReadLine() + "', ";
		}
		Query += "'A')";
		int RowsAffected = ObjCRUD.InsertRecord(Query);
		if(RowsAffected == 1)
		{
			Console.WriteLine("Inserted successfully");
		}
		else
		{
			Console.WriteLine("Error while adding details");
		}	
	}

	public static void ReadRecords()
	{
		String Query = "Select * from MyTable where Status = 'A'";
		DbDataReader Reader = ObjCRUD.ReadRecords(Query);
		int CountOfRecords = 0;
		while(Reader.Read())
		{
			for (int Index = 0; Index < FieldNames.Length; Index++)
			{
				Console.WriteLine(FieldNames[Index] + ": " + Reader.GetString(Index));
			}
			CountOfRecords++;
			Console.WriteLine("------------------------");
		}
		Console.WriteLine("Number of record(s): " + CountOfRecords);
		Reader.Close();
	}

	// Reads the records from DataTable
	// public static void ReadRecords()
	// {
	// 	String Query = "Select * from MyTable where Status = 'A'";
	// 	DataTable Table = ObjCRUD.ReadRecords(Query);
	// 	int CountOfRecords = 0;
	// 	for(int RowIndex = 0; RowIndex < Table.Rows.Count; RowIndex++)
	// 	{
	// 		for (int Index = 0; Index < FieldNames.Length; Index++)
	// 		{
	// 			Console.WriteLine(FieldNames[Index] + ": " + Table.Rows[RowIndex][FieldNames[Index]].ToString());
	// 		}
	// 		CountOfRecords++;
	// 		Console.WriteLine("--------------------------");
	// 	}
	// 	Console.WriteLine("Number of record(s): " + CountOfRecords);
	// }
}

