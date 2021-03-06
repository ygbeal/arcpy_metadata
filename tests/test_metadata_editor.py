from __future__ import print_function

__author__ = 'nickrsan'

import datetime
import unittest
import os
import shutil
import arcpy
import gc

#allow to test arcpy_metadata even when it is not installed as module
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
os.sys.path.insert(0,parentdir)
import arcpy_metadata as md

temp_data_folder = os.path.join(os.path.dirname(__file__), "test_data_temp_folder")
test_data_folder = os.path.join(os.path.dirname(__file__), "test_data")



def clean_data():
    global test_data_folder
    print("Cleaning test data folder")
    if os.path.exists(temp_data_folder):  # remove the old copy of the test data
        shutil.rmtree(temp_data_folder)
    shutil.copytree(test_data_folder,
                    temp_data_folder)  # copy the directory tree so that we can get a clean copy of the data to work with and preserve the test data as clean
    test_data_folder = temp_data_folder  # set the data folder to the temp folder now


class TestExampleCode(unittest.TestCase):
    """
        To start with, let's just get a simple test in that tests the code from the perspective of how someone might use it.
        We'll do that by running the example code, which should certainly run.
    """

    def _run_example(self, feature_class):
        metadata = md.MetadataEditor(
            feature_class)  # also has a feature_layer parameter if you're working with one, but edits get saved back to the source feature class
        metadata.title.set("The metadata title!")

        generated_time = "This layer was generated on {0:s}".format(
            datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p"))

        metadata.purpose.set("Layer represents locations of the rare Snipe.")

        metadata.abstract.append("generated by ___ software")
        metadata.abstract.append(generated_time)  # .prepend also exists
        metadata.tags.add(["foo", "bar", "baz"])  # tags.extend is equivalent to maintain list semantics

        metadata.finish()  # save the metadata back to the original source feature class and cleanup. Without calling finish(), your edits are NOT saved!

        del metadata
        gc.collect()

    # TODO: for now, no assertions, we just want the code to run start to finish and we can manually check.
    #       Later, we'll make code that actually attempts to read the data back and confirms it's there
    # TODO: make sure, GDB locks get properly remove to be able to run all test directly after another.
    #       Deleting the metadata object and running the Garbage Collector doesn't seem to do anything
    #       Right now you have to run test separately ( Makes sense, since you have to check the metadata manually)

    def test_shapefile_no_meta(self):
        clean_data()
        print("Shp without metadata")
        self._run_example(os.path.join(test_data_folder, "simple_poly_no_metadata.shp"))

    def test_shapefile_with_meta(self):
        clean_data()
        print("Shp with metadata")
        self._run_example(os.path.join(test_data_folder, "simple_poly_w_base_metadata.shp"))

    def test_shapefile_without_xml(self):
        clean_data()
        print("Shp without XML File")
        self._run_example(os.path.join(test_data_folder, "simple_poly_no_xml.shp"))

    def test_feature_class_no_meta(self):
        clean_data()
        print("FC without metadata")
        self._run_example(os.path.join(test_data_folder, r"test.gdb\root_poly"))


    def test_feature_class_with_meta(self):
        clean_data()
        print("FC in dataset with metadata")
        self._run_example(os.path.join(test_data_folder, r"test.gdb\dataset\dataset_poly"))

    def test_gdb_table(self):
        clean_data()
        print("Table no metadata")
        self._run_example(os.path.join(test_data_folder, r"test.gdb\root_table"))

    def test_fc_layer(self):
        clean_data()
        print("Feature class layer")
        arcpy.MakeFeatureLayer_management(os.path.join(test_data_folder, r"test.gdb\root_poly"), "layer")
        self._run_example("layer")

    def test_layer_file(self):
        clean_data()
        print("Layer file metadata")
        self._run_example(os.path.join(test_data_folder, r"layer.lyr"))

    def test_raster_dataset(self):
        clean_data()
        print("Raster dataset")
        self._run_example(os.path.join(test_data_folder, r"test.gdb\simple_raster"))

    def test_raster_file(self):
        clean_data()
        print("Raster file")
        self._run_example(os.path.join(test_data_folder, r"simple_raster.tif"))