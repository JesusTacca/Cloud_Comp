package invertedindex;

import java.io.IOException;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;

public class InvertedIndexMapper extends Mapper<Object, Text, Text, Text> {

	public void map(Object key, Text value, Context context)
			throws IOException, InterruptedException {

		// Leer archivos correctamente
		String fileName = ((FileSplit) context.getInputSplit()).getPath().getName();

		//asignar cada grupo de palabras una key
		String [] indexKeys = value.toString().split("\\s+");

		for(String indexKey : indexKeys) {
			// dar dormato de salida para el reducer
			context.write(new Text(indexKey.toLowerCase()), new Text(fileName));
		}
	}
}
