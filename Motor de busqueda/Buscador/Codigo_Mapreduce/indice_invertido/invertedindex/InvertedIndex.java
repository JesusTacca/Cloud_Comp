package invertedindex;

import java.io.IOException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import constants.Constants;

public class InvertedIndex {
	public static void main(String[] args) throws Exception {
		Configuration conf = new Configuration();
		Job job = Job.getInstance(conf, "JobName");
		job.setJarByClass(invertedindex.InvertedIndex.class);

		deleteFolder(conf, Constants.outputPath);

		myMapReduceTask(job, Constants.inputPath, Constants.outputPath);
	}

	public static void deleteFolder(Configuration conf, String folderPath)
			throws IOException{
		// Elimina carpeta
		FileSystem fs = FileSystem.get(conf);
		Path path = new Path(folderPath);
		if(fs.exists(path)) {
			fs.delete(path,true);
		}
	}

	public static void myMapReduceTask(Job job, String inputPath, String outputPath) throws
	IllegalArgumentException,
	IOException,
	ClassNotFoundException,
	InterruptedException {
		// mapper class
		job.setMapperClass(InvertedIndexMapper.class);

		// mapper
		job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(Text.class);

		// reducer class
		job.setReducerClass(InvertedIndexReducer.class);

		// reducer
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);

		// Directorios
		FileInputFormat.addInputPath(job, new Path(Constants.inputPath));
		FileOutputFormat.setOutputPath(job, new Path(Constants.outputPath));

		if (!job.waitForCompletion(true))
			return;
	}
}
