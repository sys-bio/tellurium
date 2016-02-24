# sedx archives
Every COMBINE Archive contains at least one file, located
at the root, i.e. highest in the hierarchy of files inside
the archive. This mandatory file is called manifest.
xml. It is an XML file that contains a flat list of names
of all files constituting the archive, and it describes each
file’s type and location inside the archive.

A COMBINE archive is a single le containing the various documents (and in the future, references
to documents), necessary for the description of a model and all associated data and procedures. This
includes for instance, but not limited to, simulation experiment descriptions in SED-ML, all models
needed to run the simulations in SBML and their graphical representations in SBGN-ML. It is a convenient
alternative if a model source URI cannot be resolved, or if an end-user is oine.