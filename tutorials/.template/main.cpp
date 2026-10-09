#include <Ponca/Ponca>
#include "utils.hpp"

using Scalar                      = float;
static constexpr unsigned int Dim = 3;
using Point                       = Ponca::PointPositionNormal<Scalar, Dim>;
using KDTree                      = Ponca::KdTreeDense<Point>;
using WeightFilter                = Ponca::DistWeightFunc<Point, Ponca::SmoothWeightKernel<Scalar>>;

void Perform(const BaseOptions& options, const KDTree& points)
{
    const auto [min, max] = GetBounds<Point>(points.points());
    /* TOTO */
}

int main(int argc, char** argv)
{
    CLI::App app{"Template code"};
    argv = app.ensure_utf8(argv);

    BaseOptions options(app);
    CLI11_PARSE(app, argc, argv);

    Perform(options, ReadPLY<Point, KDTree>(options.input));
    return 0;
}
