package invertedindex;

import java.io.IOException;
import java.util.HashSet;
import java.util.Set;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class InvertedIndexReducer extends Reducer<Text, Text, Text, Text> {
	public void reduce(Text keyIndexWord, Iterable<Text> valuesDocumentNames, Context context)
			throws IOException, InterruptedException {
		// Se almacena en la clave valor cada vez que se repita
		Set<String> documentNames = new HashSet<String>();

		for (Text valueDocumentName : valuesDocumentNames) {
			// Duplicados no se incluye 
			documentNames.add(valueDocumentName.toString());
		}

		String indexString = new String("");

		// Concatenar y leer
		for(String valueDocumentName : documentNames) {
			indexString = new String(indexString.concat
					(valueDocumentName.replaceAll(".txt", "")).concat(" "));
		}

		indexString = new String(indexString.trim());

		context.write(keyIndexWord, new Text(indexString));
	}
}
