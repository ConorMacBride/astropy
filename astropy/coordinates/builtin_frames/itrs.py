# Licensed under a 3-clause BSD style license - see LICENSE.rst

from astropy.utils.decorators import format_doc
from astropy.coordinates.representation import CartesianRepresentation, CartesianDifferential
from astropy.coordinates.baseframe import BaseCoordinateFrame, base_doc
from astropy.coordinates.attributes import (TimeAttribute,
                                            EarthLocationAttribute)
from .utils import DEFAULT_OBSTIME, EARTH_CENTER

__all__ = ['ITRS']

doc_footer = """
    Other parameters
    ----------------
    obstime : `~astropy.time.Time`
        The time at which the observation is taken.  Used for determining the
        position of the Earth and its precession.
    location : `~astropy.coordinates.EarthLocation`
        The location on the Earth.  This can be specified either as an
        `~astropy.coordinates.EarthLocation` object or as anything that can be
        transformed to an `~astropy.coordinates.ITRS` frame. The default is the
        centre of the Earth.
"""


@format_doc(base_doc, components="", footer=doc_footer)
class ITRS(BaseCoordinateFrame):
    """
    A coordinate or frame in the International Terrestrial Reference System
    (ITRS).  This is approximately a geocentric system, although strictly it is
    defined by a series of reference locations near the surface of the Earth (the ITRF).
    For more background on the ITRS, see the references provided in the
    :ref:`astropy:astropy-coordinates-seealso` section of the documentation.

    This frame also includes frames that are defined *relative* to the center of the Earth,
    but that are offset (in both position and velocity) from the center of the Earth. You
    may see such non-geocentric coordinates referred to as "topocentric".

    Topocentric ITRS frames are convenient for observations of near Earth objects where
    stellar aberration is not included. One can merely subtract the observing site's
    EarthLocation geocentric ITRS coordinates from the object's geocentric ITRS coordinates,
    put the resulting vector into a topocentric ITRS frame and then transform to AltAz
    or HADec. The other way around is to transfrom an observed AltAz or HADec position
    to a topocentric ITRS frame and add the observing site's EarthLocation geocentric
    ITRS coordinates to yield the object's geocentric ITRS coordinates.

    Note to ILRS ephemeris users: Astropy does not currently consider relativistic
    effects of the Earth's gravatational field. Nor do the AltAz or HADec refraction
    corrections compute the change in the range due to the curved path of light through
    the atmosphere, so Astropy is no substitute for the ILRS software in these respects.

    """

    default_representation = CartesianRepresentation
    default_differential = CartesianDifferential

    obstime = TimeAttribute(default=DEFAULT_OBSTIME)
    location = EarthLocationAttribute(default=EARTH_CENTER)

    @property
    def earth_location(self):
        """
        The data in this frame as an `~astropy.coordinates.EarthLocation` class.
        """
        from astropy.coordinates.earth import EarthLocation

        cart = self.represent_as(CartesianRepresentation)
        return EarthLocation(x=cart.x, y=cart.y, z=cart.z)

# Self-transform is in intermediate_rotation_transforms.py with all the other
# ITRS transforms
